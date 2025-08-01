# 한글 깨짐 문제 해결을 위한 Word 문서 생성 스크립트
import json
from docx import Document
from docx.oxml.ns import qn

def create_korean_word_document():
    # JSON 파일에서 데이터 읽기
    with open("C:/workspace/llm_study/01.test/chap05/sec04/meeting_note_corrected.json", "r", encoding="utf-8") as f:
        meeting_note_dict = json.load(f)
    
    # Word 문서 생성
    document = Document()
    
    # 한글 폰트 설정
    document.styles['Normal'].font.name = '맑은 고딕'
    document.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), '맑은 고딕')
    
    # 제목 추가
    heading = document.add_heading('회의 내용', level=1)
    # 제목의 폰트도 설정
    for run in heading.runs:
        run.font.name = '맑은 고딕'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '맑은 고딕')
    
    # 표 생성
    table = document.add_table(rows=1, cols=2)
    table.style = 'Table Grid'
    
    # 헤더 설정
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = '화자'
    hdr_cells[1].text = '내용'
    
    # 헤더 폰트 설정
    for cell in hdr_cells:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.name = '맑은 고딕'
                run._element.rPr.rFonts.set(qn('w:eastAsia'), '맑은 고딕')
    
    # 데이터 추가
    for row in meeting_note_dict:
        row_cells = table.add_row().cells
        row_cells[0].text = row["name"]
        row_cells[1].text = row["corrected_text"]
        
        # 각 셀의 폰트 설정
        for cell in row_cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.name = '맑은 고딕'
                    run._element.rPr.rFonts.set(qn('w:eastAsia'), '맑은 고딕')
    
    # 문서 저장
    document.save('C:/workspace/llm_study/01.test/chap05/sec04/meeting_note_corrected_korean.docx')
    print("한글 폰트가 설정된 Word 문서가 저장되었습니다: meeting_note_corrected_korean.docx")

if __name__ == "__main__":
    create_korean_word_document() 