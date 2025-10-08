Digital Machine Music App Backend

**Technical Specification Document**

## Implementation Status

✅ **IMPLEMENTED** | ⚠️ **PARTIAL** | ❌ **NOT IMPLEMENTED**

---

## 1. Lyrics (Text Analysis)

**1.1. Lyrics Extraction** ✅ **IMPLEMENTED**
- **Objective:** Extract the lyrics from audio files or streaming services.

- **Input:** Audio file or stream.

- **Output:** Extracted lyrics in text format.

- **Technology Stack:**
  - **Speech-to-Text Models:** Azure Cognitive Services Speech SDK
  - **Implementation:** `app/services/lyrics_service.py`

- **Considerations:** 
  - Handle background music.
  - Deal with overlapping vocals.
  - Accuracy - 95%

—-----------------------------------------------------------------------------------------------------------------

**1.2. Language Detection** ✅ **IMPLEMENTED**
- **Objective:** Identify the language of the extracted lyrics.

- **Input:** Extracted lyrics in text format.

- **Output:** Detected language (e.g., English, Spanish).

- **Technology Stack:**
  - **Language Detection Models:** Azure Text Analytics
  - **Implementation:** `app/services/language_detector.py`

- **Considerations:** 
  - Support for multiple languages.
  - Accuracy in mixed-language lyrics varied between 80-93%

—-----------------------------------------------------------------------------------------------------------------

**1.3. Translation** ✅ **IMPLEMENTED**
- **Objective:** Translate the lyrics into another language.

- **Input:** Extracted lyrics and target language.

- **Output:** Translated lyrics.

- **Technology Stack:**
  - **Translation Models:** Azure OpenAI GPT-4.1
  - **Implementation:** `app/services/translation_service.py`

- **Considerations:** 
  - Preserve the meaning and tone of lyrics.
  - Handle idiomatic expressions.
  - Accuracy - 91%

—-----------------------------------------------------------------------------------------------------------------

**1.4. Summarization** ✅ **IMPLEMENTED**
- **Objective:** Summarize the key points or themes of the lyrics.

- **Input:** Extracted lyrics.

- **Output:** Summarized text highlighting the main themes.

- **Technology Stack:**
  - **Summarization Models:** Azure OpenAI GPT-4.1
  - **Implementation:** `app/services/summarization_service.py`

- **Considerations:** 
  - Retain the context of the song.
  - Condense without losing essential meaning.

—-----------------------------------------------------------------------------------------------------------------

**1.5. Theme Identification** ✅ **IMPLEMENTED**
- **Objective:** Identify and categorize the themes within the lyrics.

- **Input:** Extracted lyrics.

- **Output:** List of themes (e.g., love, loss, celebration).

- **Technology Stack:**
  - **Topic Modeling:** Azure OpenAI GPT-4.1
  - **Implementation:** `app/services/theme_identification_service.py`

- **Considerations:** 
  - Multi-theme classification.
  - Context-aware analysis.
  - Accuracy: Enhanced with GPT-4.1

—-----------------------------------------------------------------------------------------------------------------

**1.6. Keyword Extraction** ✅ **IMPLEMENTED**
- **Objective:** Extract significant keywords from the lyrics.

- **Input:** Extracted lyrics.

- **Output:** List of keywords.

- **Technology Stack:**
  - **Keyword Extraction Models:** Azure OpenAI GPT-4.1
  - **Implementation:** `app/services/keyword_extraction_service.py`

- **Considerations:** 
  - Focus on thematic words.
  - Handle repetitive phrases.

—-----------------------------------------------------------------------------------------------------------------

**1.7. Segmentation (Chorus, Verse)** ✅ **IMPLEMENTED**
- **Objective:** Segment the lyrics into parts like chorus, verse, etc.

- **Input:** Extracted lyrics or audio file.

- **Output:** Segmented lyrics with labels (chorus, verse).

- **Technology Stack:**
  - **Segmentation Models:** Azure OpenAI GPT-4.1
  - **Implementation:** `app/services/segmentation_service.py`

- **Considerations:** 
  - High accuracy in distinguishing segments.
  - Flexibility in labeling parts.

—-----------------------------------------------------------------------------------------------------------------

#### **1.8. Sentiment Analysis** ✅ **IMPLEMENTED**
- **Objective:** Analyze the sentiment conveyed in the lyrics.

- **Input:** Extracted lyrics.

- **Output:** Sentiment score (e.g., positive, negative, neutral).

- **Technology Stack:**
  - **Sentiment Analysis Models:** Azure OpenAI GPT-4.1
  - **Implementation:** `app/services/sentiment_analysis_service.py`

- **Considerations:** 
  - Contextual sentiment analysis.
  - Differentiation between lyrical sentiment and musical tone.

—------------------------------------------------------------------------------------------------------------------

## 2. Music (Sound Analysis)

#### **2.1. Instrument Detection** ✅ **IMPLEMENTED**
- **Objective:** Detect the instruments used in the song.

- **Input:** Audio file or stream.

- **Output:** List of detected instruments.

- **Technology Stack:**
  - **Instrument Classification Models:** OpenUnmix
  - **Implementation:** `app/services/instrument_detection.py`

- **Considerations:** 
  - Handle polyphonic music.
  - Support for a wide range of instruments.

—------------------------------------------------------------------------------------------------------------------

#### **2.2. Scale & Key Detection** ✅ **IMPLEMENTED**
- **Objective:** Determine the musical scale and key of the song.

- **Input:** Audio file or stream.

- **Output:** Identified scale and key.

- **Technology Stack:**
  - **Music Theory Models:** Librosa
  - **Implementation:** `app/services/scale_key_detection_service.py`

- **Considerations:** 
  - Accuracy in detecting complex keys.
  - Adaptability to various musical genres.

#### **2.3. Genre/Subgenre Classification** ✅ **IMPLEMENTED**
- **Objective:** Classify the song into a genre or subgenre.

- **Input:** Audio file or stream.

- **Output:** Identified genre/subgenre.

- **Technology Stack:**
  - **Genre Classification Models:** Azure OpenAI GPT-4.1 + Librosa features
  - **Implementation:** `app/services/genre_classification_service.py`

- **Considerations:** 
  - Fine-grained genre classification.
  - Support for multi-genre songs.

—------------------------------------------------------------------------------------------------------------------

#### **2.4. BPM (Beats Per Minute) Detection** ✅ **IMPLEMENTED**
- **Objective:** Calculate the BPM of the song.

- **Input:** Audio file or stream.

- **Output:** BPM value.

- **Technology Stack:**
  - **BPM Detection Models:** Aubio
  - **Implementation:** `app/services/bpm_detection_service.py`

- **Considerations:** 
  - Accuracy in varying tempo songs.
  - Handle complex time signatures.

—------------------------------------------------------------------------------------------------------------------

#### **2.5. Melody & Chords Detection** ✅ **IMPLEMENTED**
- **Objective:** Extract melody and chord progression from the song.

- **Input:** Audio file or stream.

- **Output:** Notation or MIDI file of melody and chords.

- **Technology Stack:**
  - **Melody Extraction Models:** CREPE, Essentia
  - **Implementation:** `app/services/melody_chords_detection_service.py`

- **Considerations:** 
  - High precision in melody extraction.
  - Accurate chord detection in complex compositions.

—------------------------------------------------------------------------------------------------------------------

#### **2.6. Melody Sentiment Analysis** ✅ **IMPLEMENTED**
- **Objective:** Analyze the sentiment conveyed through the melody.

- **Input:** Melody extracted from the song.

- **Output:** Sentiment score (e.g., happy, sad).

- **Technology Stack:**
  - **Melody Analysis Models:** Azure OpenAI GPT-4.1 + Librosa
  - **Implementation:** Integrated in `app/services/sentiment_analysis_service.py`

- **Considerations:** 
  - Correlate melody with mood.
  - Handle ambiguous sentiment in melody.

—------------------------------------------------------------------------------------------------------------------

### **3. Music Transposition** ❌ **NOT IMPLEMENTED**

#### **3.1. Transcription** ❌ **NOT IMPLEMENTED**
- **Objective:** Generate sheet music for each instrument in the song.

- **Input:** Audio file or stream.

- **Output:** Music sheet in standard notation or MIDI.

- **Technology Stack:**
  - **Transcription Models:** Onsets and Frames, Melody RNN.
  - **APIs:** Google Magenta, MuseScore.

- **Considerations:** 
  - Support for polyphonic transcription.
  - Accuracy in capturing rhythmic and pitch details.

—------------------------------------------------------------------------------------------------------------------

#### **3.2. Transposition & Voice Cancelling** ❌ **NOT IMPLEMENTED**
- **Objective:** Transpose the song to a different key and cancel specific voices or instruments.

- **Input:** Audio file or stream.

- **Output:** Transposed audio and/or audio with certain elements removed.

- **Technology Stack:**
  - **Voice Cancelling Models:** Open Unmix, Spleeter.
  - **APIs:** Custom deep learning models, Librosa.

- **Considerations:** 
  - Maintain audio quality after transposition.
  - Flexibility in isolating and removing specific elements.

—------------------------------------------------------------------------------------------------------------------

#### **3.3. BPM & Key Modification** ❌ **NOT IMPLEMENTED**
- **Objective:** Modify the BPM or key of the song.

- **Input:** Audio file or stream.

- **Output:** Audio file with modified BPM or key.

- **Technology Stack:**
  - **Tempo and Key Adjustment Models:** Rubber Band Library, PitchShift.
  - **APIs:** Custom Python scripts, Essentia.

- **Considerations:** 
  - Preserve the natural sound after modification.
  - Handle extreme changes without audio distortion.

## Current Implementation Status Summary

- **Total Features**: 17
- **Implemented**: 14 (82%)
- **Not Implemented**: 3 (18%)

### ✅ Fully Implemented Features (14/17):
1. ✅ Lyrics Extraction
2. ✅ Language Detection  
3. ✅ Translation
4. ✅ Summarization
5. ✅ Theme Identification
6. ✅ Keyword Extraction
7. ✅ Segmentation
8. ✅ Sentiment Analysis
9. ✅ Instrument Detection
10. ✅ Scale & Key Detection
11. ✅ Genre Classification
12. ✅ BPM Detection
13. ✅ Melody & Chords Detection
14. ✅ Melody Sentiment Analysis

### ❌ Missing Features (3/17):
1. ❌ Transcription
2. ❌ Transposition & Voice Cancelling
3. ❌ BPM & Key Modification

## API Documentation

See `API_DOCUMENTATION.md` for complete API reference and usage examples.

