# Overview

Quiz Playground is a Flask-based educational platform that combines quiz-based learning with interactive gaming. The application allows teachers to create, manage, and deploy quizzes that students can access through various embedded games. The platform features AI-powered question generation using OpenAI, YouTube video integration for content-based assessments, and a comprehensive user management system with premium subscription capabilities.

The system serves as a gamified formative assessment tool where students can play games while answering quiz questions, making learning more engaging and interactive. Teachers can create custom quizzes, generate questions from YouTube videos or text content, and track student performance through detailed analytics.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Architecture
The application is built on Flask as the primary web framework, providing a lightweight and flexible foundation for the web application. The main application logic is centralized in `main.py`, which handles routing, request processing, and integration with various services. The database setup is managed through `setup_database.py`, which configures the PostgreSQL database schema and initializes required tables.

## Database Design
The system uses PostgreSQL as the primary database, accessed through the pg8000 driver. The database schema includes core tables for user management (`users`), quiz content (`complete_questions`), and educational resources. The `users` table stores teacher information including subscription status, authentication details, and profile data. The `complete_questions` table maintains quiz content with support for multiple-choice questions, correct answers, and quiz metadata.

## Authentication and Authorization
User authentication is implemented through a combination of email/password credentials and Google OAuth integration. The system includes support for two-factor authentication (TFA) and maintains session management for user security. Premium subscription functionality is integrated with Stripe for payment processing, enabling feature differentiation between free and paid accounts.

## AI Integration
The platform leverages OpenAI's API for intelligent question generation, allowing teachers to automatically create quiz questions from educational content. This feature supports content extraction from YouTube videos using the YouTube Transcript API and PyTube library, enabling automated quiz creation from video content.

## Game Integration Architecture
The system hosts multiple embedded games built with different technologies:
- Godot Engine games (ActionAdventure, Arthur, Asteroido, Cannon, Climb, Memory) compiled to WebAssembly
- P5.js games (CoinDash) with P5Play physics engine integration
- Kaplay framework games (Pong) for simple arcade-style interactions

Each game is designed to consume quiz data through a standardized interface, allowing any quiz to be played in any game format.

## Content Management
Quiz content can be created through multiple methods:
- Manual question entry through web forms
- AI-powered generation from text or YouTube content
- Bulk upload via CSV files
- YouTube video integration with automatic transcript processing

## Data Storage Solutions
The application uses multiple storage mechanisms:
- PostgreSQL database for structured quiz and user data
- Replit Object Storage for file uploads and media assets
- Local file system for temporary processing and game assets
- JSON files for quiz data exchange and backup

# External Dependencies

## Core Services
- **PostgreSQL Database**: Primary data storage for users, quizzes, and application state
- **OpenAI API**: Powers AI question generation from text and video content
- **Google OAuth**: Provides secure user authentication and account management
- **Stripe Payment Processing**: Handles premium subscription billing and management
- **YouTube Data API**: Enables video content integration and transcript extraction

## Communication Services
- **Twilio**: SMS/phone-based communication and verification services
- **Email Services**: Integration capabilities for user notifications and account management

## Frontend Libraries and Frameworks
- **Bootstrap 5**: Primary UI framework for responsive design and component styling
- **DataTables**: Advanced table functionality for quiz and user data presentation
- **jQuery**: DOM manipulation and AJAX request handling

## Game Development Frameworks
- **Godot Engine**: Primary game engine for complex interactive educational games
- **P5.js with P5Play**: Canvas-based game development with physics simulation
- **Kaplay**: Lightweight game framework for simple arcade-style interactions
- **Planck.js**: Physics engine integration for realistic game mechanics

## Development and Deployment
- **Flask Framework**: Core web application framework with templating support
- **Werkzeug**: WSGI utilities for secure file handling and request processing
- **Flask-Sitemapper**: SEO optimization through automatic sitemap generation
- **pg8000**: Pure Python PostgreSQL database adapter for reliable data access

## Media Processing
- **PyTube**: YouTube video data extraction and metadata processing
- **YouTube Transcript API**: Automatic transcript extraction for content analysis
- **HTML Processing Libraries**: Content sanitization and text extraction utilities

The architecture supports scalable content delivery through CDN integration for static assets and implements caching strategies for improved performance across the gaming and quiz platforms.