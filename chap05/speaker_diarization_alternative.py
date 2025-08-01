#!/usr/bin/env python3
"""
Alternative Speaker Diarization Implementation
This script provides a simple speaker diarization approach that doesn't require
special Hugging Face model permissions.
"""

import numpy as np
import librosa
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import torch
import torchaudio
import warnings
warnings.filterwarnings('ignore')

def simple_speaker_diarization(audio_path, num_speakers=2, sr=16000):
    """
    Simple speaker diarization using MFCC features and K-means clustering
    
    Args:
        audio_path (str): Path to the audio file
        num_speakers (int): Number of speakers to detect
        sr (int): Sample rate for audio processing
    
    Returns:
        list: List of dictionaries containing speaker segments
    """
    print(f"Processing audio file: {audio_path}")
    
    # Load audio
    y, sr = librosa.load(audio_path, sr=sr)
    print(f"Audio loaded: {len(y)/sr:.2f} seconds, {sr} Hz")
    
    # Extract MFCC features
    print("Extracting MFCC features...")
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_delta = librosa.feature.delta(mfcc)
    mfcc_delta2 = librosa.feature.delta(mfcc, order=2)
    
    # Combine features
    features = np.vstack([mfcc, mfcc_delta, mfcc_delta2])
    features = features.T  # Transpose to get (time, features)
    
    print(f"Feature shape: {features.shape}")
    
    # Normalize features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Cluster
    print(f"Clustering into {num_speakers} speakers...")
    kmeans = KMeans(n_clusters=num_speakers, random_state=42, n_init=10)
    speaker_labels = kmeans.fit_predict(features_scaled)
    
    # Convert to time segments
    frame_duration = librosa.frames_to_time(1, sr=sr)
    segments = []
    
    current_speaker = speaker_labels[0]
    start_time = 0
    
    for i, label in enumerate(speaker_labels):
        if label != current_speaker:
            end_time = i * frame_duration
            segments.append({
                'speaker': f"Speaker_{current_speaker}",
                'start': start_time,
                'end': end_time,
                'duration': end_time - start_time
            })
            current_speaker = label
            start_time = end_time
    
    # Add final segment
    segments.append({
        'speaker': f"Speaker_{current_speaker}",
        'start': start_time,
        'end': len(y) / sr,
        'duration': (len(y) / sr) - start_time
    })
    
    return segments

def print_segments(segments):
    """Print speaker segments in a readable format"""
    print("\n" + "="*60)
    print("SPEAKER DIARIZATION RESULTS")
    print("="*60)
    
    for i, segment in enumerate(segments):
        print(f"Segment {i+1:2d}: {segment['speaker']:12s} "
              f"({segment['start']:6.2f}s - {segment['end']:6.2f}s) "
              f"[{segment['duration']:5.2f}s]")
    
    print("="*60)
    
    # Summary statistics
    speaker_stats = {}
    for segment in segments:
        speaker = segment['speaker']
        if speaker not in speaker_stats:
            speaker_stats[speaker] = {'total_time': 0, 'segments': 0}
        speaker_stats[speaker]['total_time'] += segment['duration']
        speaker_stats[speaker]['segments'] += 1
    
    print("\nSPEAKER SUMMARY:")
    for speaker, stats in speaker_stats.items():
        print(f"{speaker}: {stats['segments']} segments, "
              f"{stats['total_time']:.2f}s total")

def main():
    """Main function to demonstrate speaker diarization"""
    print("Alternative Speaker Diarization")
    print("="*40)
    
    # Check for available audio files
    import os
    audio_dir = "audio"
    
    if os.path.exists(audio_dir):
        audio_files = [f for f in os.listdir(audio_dir) 
                      if f.endswith(('.mp3', '.wav', '.m4a'))]
        
        if audio_files:
            print(f"Found audio files: {audio_files}")
            
            # Process the first audio file
            audio_path = os.path.join(audio_dir, audio_files[0])
            print(f"\nProcessing: {audio_path}")
            
            try:
                segments = simple_speaker_diarization(audio_path, num_speakers=2)
                print_segments(segments)
                
                # Save results to file
                output_file = f"diarization_results_{audio_files[0].split('.')[0]}.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write("Speaker Diarization Results\n")
                    f.write("="*40 + "\n")
                    for i, segment in enumerate(segments):
                        f.write(f"Segment {i+1}: {segment['speaker']} "
                               f"({segment['start']:.2f}s - {segment['end']:.2f}s)\n")
                
                print(f"\nResults saved to: {output_file}")
                
            except Exception as e:
                print(f"Error processing audio: {e}")
        else:
            print("No audio files found in audio/ directory")
            print("Please place audio files in the audio/ directory")
    else:
        print("Audio directory not found")
        print("Please create an 'audio' directory and place audio files there")

if __name__ == "__main__":
    main() 