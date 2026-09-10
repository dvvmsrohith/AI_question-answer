# 🤖 AI Question Answering System

An AI-powered web application that answers questions based on a given paragraph using a pretrained Natural Language Processing (NLP) model.

## 📌 Project Overview

The AI Question Answering System allows users to enter a paragraph and ask a question related to that paragraph.

The application uses the Hugging Face Transformers library and a pretrained DistilBERT model to understand the paragraph and identify the most relevant answer.

The application also stores previous questions and answers permanently using SQLite, allowing users to view their question history and navigate between saved questions.

## 🚀 Features

- 🤖 AI-powered question answering
- 📄 Enter any paragraph or passage
- ❓ Ask questions based on the paragraph
- 💡 Generates answers automatically
- 📊 Displays AI confidence score
- 💾 Permanently saves questions and answers
- 🗄️ SQLite database for question history
- 📚 View previously asked questions
- ⬅️ Previous question navigation
- ➡️ Next question navigation
- 🌐 Simple and responsive web interface
- 🔐 No paid API required
- 🧠 Uses a pretrained NLP model

## 🛠️ Technologies Used

- Python
- Flask
- Hugging Face Transformers
- PyTorch
- SQLite
- HTML
- CSS
- Jinja2

## 🤖 AI Model

### Model

`distilbert-base-cased-distilled-squad`

The model is a DistilBERT-based question answering model fine-tuned on the SQuAD (Stanford Question Answering Dataset) dataset.

It receives two inputs:

1. **Question**
2. **Context (Paragraph)**

The model analyzes the paragraph and extracts the most relevant answer to the question.

## 🔄 How It Works

```text
User enters Paragraph
        ↓
User enters Question
        ↓
Flask receives the input
        ↓
Hugging Face QA Model
        ↓
AI analyzes the paragraph
        ↓
Answer + Confidence Score
        ↓
Saved in SQLite Database
        ↓
Displayed to the User
