# Tasks: RAG Pipeline Phase 4: FastAPI Backend and Frontend Integration

**Input**: Design documents from `/specs/004-fastapi-backend/`
**Prerequisites**: plan.md, spec.md

## Phase 1: Setup
- [x] T001 Install FastAPI and Uvicorn dependencies
- [x] T002 Create api.py in root directory

## Phase 2: Backend Implementation
- [x] T003 Initialize FastAPI app with CORS for localhost in api.py
- [x] T004 Import agent from agent.py and create POST /chat endpoint
- [x] T005 Return agent responses as JSON from /chat endpoint

## Phase 3: Frontend Integration
- [x] T006 Update Chatbot component to fetch from http://127.0.0.1:8000/chat
- [x] T007 Implement full chat interface with input, message history, send button

## Phase 4: Testing
- [x] T008 Test backend API functionality
- [x] T009 Test frontend-backend integration