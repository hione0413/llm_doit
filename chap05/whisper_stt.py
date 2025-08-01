import os
import torch
import pandas as pd
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from pyannote.audio import Pipeline

os.environ["PATH"] += os.pathsep + r"C:\workspace\llm_study\ffmpeg-2025-07-31\bin"

def whisper_stt(
    audio_file_path: str, 
    output_file_path: str = "./output/whisper_stt.csv"):

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = "openai/whisper-large-v3-turbo"

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch_dtype,
        device=device,
        return_timestamps=True, # MP3 파일을 청크 단위로 나누고 청크 시간을 각각 기록 -> 화자 분리 기능에 유용
        chunk_length_s=10, # 오디오 파일을 10초씩 나눠 처리
        stride_length_s=2, # 각 청크가 2초씩 겹치도록 설정 -> 분석의 정확도 향상 기대
    )

    result = pipe(audio_file_path)
    df = whisper_to_dataframe(result, output_file_path)

    return result, df

def whisper_to_dataframe(result, output_file_path):
    # chunks 를 CSV 파일로 저장
    start_end_text = []

    for chunk in result['chunks']:
        start_time = chunk['timestamp'][0]
        end_time = chunk['timestamp'][1]
        text = chunk['text']
        start_end_text.append([start_time, end_time, text])
        df = pd.DataFrame(start_end_text, columns=['start_time', 'end_time', 'text'])
        df.to_csv(output_file_path, index=False, sep='\t')

    return df


def speaker_diarization(
    audio_file_path: str, 
    output_rttm_path: str = "./output/speaker_diarization.rttm",
    output_csv_path: str = "./output/speaker_diarization.csv",
    ):

    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token="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"
    )

    # CUDA 를 사용할 수 있다면 사용하도록 설정
    # 즉, NVIDIA GPU 를 사용할 수 있는지 확인
    import torch

    if torch.cuda.is_available():
        pipeline.to(torch.device("cuda"))
        print('cuda is available')
    else:
        print('cuda is not available')
    
    # Run the pipeline on an audio file
    diarization = pipeline(audio_file_path)

    # dump the diarization output to disk using RTTM format
    with open(output_rttm_path, "w", encoding="utf-8") as rttm:
        diarization.write_rttm(rttm)
    
    df_rttm = pd.read_csv(
        output_rttm_path, 
        sep=' ', 
        header=None,
        names=['type', 'file_id', 'channel', 'start_time', 'duration', 'C1', 'C2', 'speeker_id', 'C3', 'C4']
    )

    # start + duration 을 end 로 변환
    df_rttm['end_time'] = df_rttm['start_time'] + df_rttm['duration']

    # speaker_id 를 기반으로 화자별 구간 나누기
    df_rttm["number"] = None # number 열을 만들고 None 으로 초기화
    df_rttm.at[0, "number"] = 0 # 첫 번째 행의 number 열을 0로 설정

    for i in range(1, len(df_rttm)):
        if df_rttm.at[i, "speeker_id"] != df_rttm.at[i-1, "speeker_id"]:
            df_rttm.at[i, "number"] = df_rttm.at[i-1, "number"] + 1
        else:
            df_rttm.at[i, "number"] = df_rttm.at[i-1, "number"]

    df_rttm_grouped = df_rttm.groupby("number").agg(
        start=pd.NamedAgg(column='start_time', aggfunc="min"),
        end=pd.NamedAgg(column='end_time', aggfunc="max"),
        speaker=pd.NamedAgg(column='speeker_id', aggfunc="first")
    )

    df_rttm_grouped['duration'] = df_rttm_grouped['end'] - df_rttm_grouped['start']
    df_rttm_grouped = df_rttm_grouped.reset_index(drop=True)

    df_rttm_grouped.to_csv(output_csv_path, index=False, sep=',')

    return df_rttm_grouped


def stt_to_rttm(
    audio_file_path: str,
    whisper_output_file_path: str,
    rttm_output_file_path: str,
    csv_output_file_path: str,
    final_output_file_path: str,
    ):

    # whisper: 음성 추출
    result, df_stt = whisper_stt(audio_file_path, whisper_output_file_path)
    
    # diarization: 화자별 분리, 음성 대화 내용은 없음
    df_rttm_grouped = speaker_diarization(
        audio_file_path,
        rttm_output_file_path,
        csv_output_file_path
    )

    df_rttm_grouped["text"] = ""

    for i_stt, row_stt in df_stt.iterrows():
        overlap_dict = {}
        for i_rttm, row_rttm in df_rttm_grouped.iterrows():
            overlap = max(0, min(
                row_stt["end_time"], row_rttm["end"]) - max(row_stt["start_time"], row_rttm["start"]))
            overlap_dict[i_rttm] = overlap

        max_overlap = max(overlap_dict.values())
        max_overlap_key = max(overlap_dict, key=overlap_dict.get)

        if max_overlap > 0:
            df_rttm_grouped.at[max_overlap_key, "text"] += row_stt["text"] + "\n"

    df_rttm_grouped.to_csv(final_output_file_path, index=False, sep=',', encoding='utf-8')

    return df_rttm_grouped


if __name__ == "__main__":
    file_name = "싼기타_비싼기타"
    audio_file_path = f"./chap05/audio/{file_name}.mp3"
    whisper_output_file_path = f"./chap05/stt_result/{file_name}_whisper_stt.csv"
    rttm_output_file_path = f"./chap05/stt_result/{file_name}_speaker_diarization.rttm"
    csv_output_file_path = f"./chap05/stt_result/{file_name}_speaker_diarization.csv"
    final_output_file_path = f"./chap05/stt_result/{file_name}_stt_to_rttm_final.csv"

    # whisper: 음성 추출
    # result, df = whisper_stt(audio_file_path, whisper_output_file_path)
    # print(result)
    # print(df)

    # diarization: 화자별 분리, 음성 대화 내용은 없음
    # df_rttm_grouped = speaker_diarization(
    #     audio_file_path,
    #     rttm_output_file_path,
    #     csv_output_file_path
    # )
    #
    # print(df_rttm_grouped)

    df_rttm_grouped = stt_to_rttm(
        audio_file_path,
        whisper_output_file_path,
        rttm_output_file_path,
        csv_output_file_path,
        final_output_file_path
    )

    print(df_rttm_grouped)


