# Contract Parser

An automated contract and compliance document parser powered by AI.

Upload a PDF contract → AI extracts key entities → Returns structured JSON → Saved to database.

## 🚀 Live Demo
👉 [Main Program LINK](https://contract-parser.onrender.com)
📖 API Docs: [API DOCS LINK](https://contract-parser.onrender.com/docs)

---

## Why This Exists

Every business drowns in PDFs. Contracts, invoices, NDAs, supply agreements, 
They all contain critical information locked inside unstructured text that no
database can query and no system can act on automatically.

The traditional solution is paying lawyers to read every document and manually 
enter the data. That is slow, expensive, and prone to missing important details.

Contract Parser solves this by combining modern PDF extraction with large 
language models to automatically identify and pull out the information that 
actually matters - in seconds, not hours.

## Who This Is Built For

**SaaS Startups** — Any platform that handles user-submitted documents, 
onboarding agreements, or vendor contracts, can plug this pipeline in to 
automate data extraction instead of relying on manual review.

**Legal Teams** — Instead of reading a 40-page contract to find the termination 
clause or governing law, upload it and get the answer in under 10 seconds.

**Finance & Procurement** — Instantly extract payment terms, dollar amounts, 
and party obligations from supplier contracts and invoices without opening 
a single PDF manually.

**Compliance Departments** — Flag missing fields, identify key obligations, 
and build an auditable record of every contract your organization has processed.

## The Problem It Solves

80% of SaaS companies have this exact problem: unstructured documents coming 
in from users, clients, or partners that need to be processed, understood, 
and stored in a way that is actually usable. Building a custom AI pipeline 
to handle this used to require a data science team. This project shows it 
can be done cleanly with the right tools.

## Tech Stack
- **Python + FastAPI** — Backend API and server
- **pdfplumber** — PDF text extraction
- **Google Gemini API** — AI entity extraction with strict JSON output
- **SQLite** — Structured storage of parsed results
- **Render** — Cloud deployment

## Features
- Upload any text-based PDF contract
- AI extracts: parties, dates, dollar amounts, obligations, termination clauses
- Structured JSON output saved to database
- Clean and simple frontend UI with loading states
- Error handling for invalid files, scanned PDFs, and API failures
- Auto-rejects non-PDF uploads
- Live deployed — no setup required to try it
