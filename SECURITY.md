# Security — v1

**Version:** 1.0
**Last Updated:** February 2026

This document covers the **security considerations** for the Phi-2 Chatbot GUI.

---

## 1. Offline Operation

* The chatbot runs **entirely locally** on your machine.
* **No data is sent to any server**; all messages, history, and logs stay on your computer.
* Model files (`.gguf`) are loaded from your local storage and never downloaded by the application itself.

> ✅ This drastically reduces exposure to network-based attacks or data leaks.

---

## 2. User Data

* Chat history is stored **only in memory** during runtime.
* If you use **Save Chat**, it creates a **plaintext `.txt` file** wherever you choose.
* You are responsible for securing these files; the app does **not encrypt saved chats**.

> ⚠️ Do not share sensitive information in chats unless you are comfortable storing it unencrypted locally.

---

## 3. Model Files

* The app requires a **GGUF model file**, e.g., `phi-2.Q4_K_M.gguf`.
* Download only from **trusted sources**, like the official Hugging Face link:
  [https://huggingface.co/codegood/phi-2-Q4_K_M-GGUF/tree/main](https://huggingface.co/codegood/phi-2-Q4_K_M-GGUF/tree/main)
* Malicious models could theoretically execute code or compromise your system, so **verify source authenticity**.

---

## 4. Dependencies

* `customtkinter` — for GUI rendering
* `llama-cpp-python` — for local LLaMA model inference

> Install dependencies via `pip install -r requirements.txt`.
> Always use the **official Python package repositories** to reduce risk of malicious packages.

---

## 5. Security Limitations

1. **Plaintext storage**: Chat logs are not encrypted.
2. **Local execution only**: No sandboxing; malicious code could execute if introduced via a model or dependency.
3. **CPU-only inference**: Resource exhaustion attacks are limited to your machine’s CPU/RAM.

> 🛡️ In other words, the main risk comes from untrusted model files or manually modified code. Do not run code/models from unknown sources.

---

## 6. Recommendations

* Always keep a **backup** of your important chat logs.
* **Do not share sensitive personal data** with the chatbot.
* Only use **trusted GGUF models** from verified sources.
* Keep Python and dependencies up to date.

---

## 7. Future Updates

* This is **v1**, and will **only be updated upon request** or if a contributor submits security improvements.
* Any new release will explicitly note **changes to security practices**.

---

> **Summary:** Phi-2 Chatbot GUI is designed to run **offline safely**, but the security of saved chat logs and model files depends on the user. Treat models and files from untrusted sources with caution.

---
