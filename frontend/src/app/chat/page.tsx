"use client";

import { useState, useRef, useEffect } from "react";
import Link from "next/link";

interface Message {
  role: "user" | "assistant";
  content: string;
  tier?: string;
  source?: string;
  redirect_url?: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "হ্যালো! আমি EduQ। আপনার পড়াশোনা, হোমওয়ার্ক বা যেকোনো শিক্ষামূলক বিষয়ে সাহায্য করতে আমি প্রস্তুত। আপনার প্রশ্নটি লিখুন!",
      source: "EduQ AI",
      tier: "system",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  
  const [sessionId, setSessionId] = useState("default_session");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setSessionId("session_" + Math.random().toString(36).substring(2, 9));
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const query = input.trim();
    if (!query || loading) return;

    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: query }]);
    setLoading(true);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
      const res = await fetch(`${apiUrl}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, session_id: sessionId }),
      });

      if (!res.ok) throw new Error("Backend error");

      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.response,
          tier: data.tier,
          source: data.source,
          redirect_url: data.redirect_url,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "দুঃখিত, ব্যাকএন্ড সার্ভারের সাথে সংযোগ স্থাপন করা যায়নি। অনুগ্রহ করে নিশ্চিত করুন ব্যাকএন্ড চালু রয়েছে।",
          source: "Connection Error",
          tier: "error",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-slate-50 font-sans">
      {/* Header */}
      <header className="bg-emerald-700 text-white px-6 py-4 shadow-sm flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link href="/" className="text-emerald-200 hover:text-white transition-colors text-sm font-medium">
            ← Back
          </Link>
          <div>
            <h1 className="text-xl font-bold tracking-tight flex items-center gap-2">
              EduQ <span className="text-xs bg-emerald-800 text-emerald-200 px-2 py-0.5 rounded-full font-normal">AI</span>
            </h1>
            <p className="text-xs text-emerald-200">Your Smart Learning Companion</p>
          </div>
        </div>
        <div className="text-xs text-emerald-100 bg-emerald-800/80 px-3 py-1.5 rounded-lg border border-emerald-600/50">
          Smart Learning • Homework Help • Exam Prep
        </div>
      </header>

      {/* Messages */}
      <main className="flex-1 overflow-y-auto px-4 py-6 max-w-3xl w-full mx-auto space-y-4">
        {messages.map((m, idx) => (
          <div key={idx} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm shadow-sm ${
                m.role === "user"
                  ? "bg-emerald-600 text-white rounded-br-none"
                  : "bg-white text-slate-800 border border-slate-200 rounded-bl-none"
              }`}
            >
              <p className="whitespace-pre-wrap leading-relaxed">{m.content}</p>

              {m.redirect_url && (
                <div className="mt-2.5">
                  <a
                    href={m.redirect_url}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-block text-xs font-semibold bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border border-emerald-200 rounded-md px-2.5 py-1"
                  >
                    পোর্টাল ভিজিট করুন ↗
                  </a>
                </div>
              )}

              {m.role === "assistant" && m.source && (
                <div className="mt-2 pt-1.5 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-400">
                  <span>উৎস: {m.source}</span>
                  {m.tier && <span className="uppercase font-mono text-[9px] bg-slate-100 px-1.5 py-0.5 rounded text-slate-500">{m.tier}</span>}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-white border border-slate-200 rounded-2xl rounded-bl-none px-4 py-3 text-sm text-slate-500 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
              EduQ উত্তর প্রস্তুত করছে...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </main>

      {/* Input Form */}
      <footer className="bg-white border-t border-slate-200 p-4">
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="প্রশ্ন লিখুন (বাংলা বা ইংরেজি)..."
            className="flex-1 border border-slate-300 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent text-slate-800"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-emerald-700 hover:bg-emerald-800 disabled:opacity-50 text-white font-medium px-5 py-2.5 rounded-xl text-sm transition-colors"
          >
            পাঠান
          </button>
        </form>
      </footer>
    </div>
  );
}