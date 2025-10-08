# Music App API Documentation

## Overview
The Music App provides comprehensive audio analysis capabilities including lyrics extraction, music analysis, and various AI-powered text processing features.

## Available Features

### 1. Lyrics Analysis Features

#### 1.1 Lyrics Extraction
- **Feature ID**: `lyrics_extraction`
- **Description**: Extract lyrics from audio files using Azure Speech Services
- **Technology**: Azure Cognitive Services Speech SDK

#### 1.2 Language Detection
- **Feature ID**: `language_detection`
- **Description**: Detect the language of extracted lyrics
- **Technology**: Azure Text Analytics
- **Dependencies**: Requires lyrics extraction

#### 1.3 Translation
- **Feature ID**: `translation`
- **Description**: Translate lyrics to target language
- **Technology**: Azure OpenAI GPT-4.1
- **Parameters**: `target_language` (default: "English")
- **Dependencies**: Requires lyrics extraction

#### 1.4 Summarization
- **Feature ID**: `summarization`
- **Description**: Summarize lyrics content
- **Technology**: Azure OpenAI GPT-4.1
- **Parameters**: `summary_type` ("comprehensive" or "short")
- **Dependencies**: Requires lyrics extraction

#### 1.5 Theme Identification
- **Feature ID**: `theme_identification`
- **Description**: Identify themes in lyrics
- **Technology**: Azure OpenAI GPT-4.1
- **Dependencies**: Requires lyrics extraction

#### 1.6 Keyword Extraction
- **Feature ID**: `keyword_extraction`
- **Description**: Extract significant keywords from lyrics
- **Technology**: Azure OpenAI GPT-4.1
- **Dependencies**: Requires lyrics extraction

#### 1.7 Segmentation
- **Feature ID**: `segmentation`
- **Description**: Segment lyrics into verses, chorus, bridge, etc.
- **Technology**: Azure OpenAI GPT-4.1
- **Dependencies**: Requires lyrics extraction

#### 1.8 Sentiment Analysis
- **Feature ID**: `sentiment_analysis`
- **Description**: Analyze sentiment of lyrics
- **Technology**: Azure OpenAI GPT-4.1
- **Dependencies**: Requires lyrics extraction

### 2. Music Analysis Features

#### 2.1 Instrument Detection
- **Feature ID**: `instrument_detection`
- **Description**: Detect instruments used in the song
- **Technology**: OpenUnmix model

#### 2.2 Scale & Key Detection
- **Feature ID**: `scale_key_detection`
- **Description**: Determine musical scale and key
- **Technology**: Librosa

#### 2.3 Genre Classification
- **Feature ID**: `genre_classification`
- **Description**: Classify genre/subgenre
- **Technology**: Azure OpenAI GPT-4.1 + Librosa features

#### 2.4 BPM Detection
- **Feature ID**: `bpm_detection`
- **Description**: Calculate beats per minute
- **Technology**: Aubio

#### 2.5 Melody & Chords Detection
- **Feature ID**: `melody_chords_detection`
- **Description**: Extract melody and chord progression
- **Technology**: CREPE + Essentia

#### 2.6 Melody Sentiment Analysis
- **Feature ID**: `melody_sentiment_detection`
- **Description**: Analyze sentiment from melody
- **Technology**: Azure OpenAI GPT-4.1 + Librosa

## API Endpoints

### Upload Files
```
POST /documents/upload
```

**Request**: Multipart form data
- `audio`: Audio files (mp3, wav, etc.)
- `document`: Document files (optional)
- `video`: Video files (optional)
- `url`: URL to analyze (optional)

**Response**:
```json
{
  "message": "Files uploaded successfully",
  "document_ids": ["uuid1", "uuid2", ...]
}
```

### Analyze Audio
```
POST /documents/analyze
```

**Request Body**:
```json
{
  "document_ids": ["uuid1", "uuid2"],
  "features": [
    "lyrics_extraction",
    "language_detection",
    "translation",
    "summarization",
    "theme_identification",
    "keyword_extraction",
    "segmentation",
    "sentiment_analysis",
    "instrument_detection",
    "scale_key_detection",
    "genre_classification",
    "bpm_detection",
    "melody_chords_detection",
    "melody_sentiment_detection"
  ],
  "target_language": "Spanish",
  "summary_type": "comprehensive"
}
```

**Response**:
```json
{
  "message": "Audio processed",
  "results": {
    "uuid1": {
      "lyrics_extraction": "...",
      "language_detection": {
        "detected_language": "en",
        "confidence": 0.99
      },
      "translation": {
        "original_lyrics": "...",
        "translated_lyrics": "...",
        "target_language": "Spanish"
      },
      "bpm_detection": 120.5,
      "scale_key_detection": {
        "key": "C",
        "scale": "major"
      }
    }
  }
}
```

## Configuration

### Environment Variables Setup
Create a `.env` file in the project root based on `.env.example`:

```bash
# Copy the example file
cp .env.example .env

# Edit the .env file with your actual credentials
nano .env
```

### Required Environment Variables
```bash
# Azure OpenAI API Keys (comma-separated)
AZURE_OPENAI_API_KEYS=your_key1,your_key2,your_key3

# Azure OpenAI API Base URLs (comma-separated)  
AZURE_OPENAI_API_BASES=https://endpoint1.openai.azure.com,https://endpoint2.openai.azure.com,https://endpoint3.openai.azure.com

# Azure OpenAI Deployment Name
AZURE_OPENAI_DEPLOYMENT=gpt-4.1

# Azure Text Analytics (for language detection)
AZURE_TEXT_ANALYTICS_KEY=your_text_analytics_key
AZURE_TEXT_ANALYTICS_ENDPOINT=https://your-endpoint.cognitiveservices.azure.com/

# Azure Speech Services (for lyrics extraction)  
AZURE_SPEECH_KEY=your_speech_key
AZURE_SPEECH_REGION=your_region
```

### Azure OpenAI Setup
The application uses Azure OpenAI with multiple API keys for load balancing and high availability. The service automatically rotates between keys if one fails.

## Error Handling

All services include comprehensive error handling with meaningful error messages:

```json
{
  "error": "Translation failed: Rate limit exceeded",
  "status": "error"
}
```

## Dependencies

See `requirements.txt` for complete dependency list. Key dependencies:
- Flask
- Azure Cognitive Services
- OpenAI
- Librosa
- Aubio
- CREPE
- Essentia
- OpenUnmix
- PyTorch

## Usage Examples

### Basic Audio Analysis
```bash
# Upload file
curl -X POST http://localhost:5000/documents/upload \
  -F "audio=@song.mp3"

# Analyze with basic features
curl -X POST http://localhost:5000/documents/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "document_ids": ["uuid"],
    "features": ["lyrics_extraction", "bpm_detection", "scale_key_detection"]
  }'
```

### Advanced Text Analysis
```bash
curl -X POST http://localhost:5000/documents/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "document_ids": ["uuid"],
    "features": [
      "lyrics_extraction",
      "language_detection", 
      "translation",
      "summarization",
      "sentiment_analysis"
    ],
    "target_language": "French",
    "summary_type": "short"
  }'
```
