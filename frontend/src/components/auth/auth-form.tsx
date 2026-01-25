"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth-context";

export function AuthForm({ mode }: { mode: "login" | "register" }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const { login, register } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (mode === "login") {
        await login({ email, password }); 
      } else {
        await register({ email, password });
      }

      // We use window.location.href to FORCE the browser to go to the dashboard.
      // This bypasses any Next.js "stuck" state.
      window.location.href = "/dashboard";

    } catch (error: any) {
      console.error("Auth error:", error);
      alert(error.message || "Something went wrong. Check the console.");
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="w-full space-y-6 bg-white p-2">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-[10px] font-black uppercase tracking-widest text-slate-400 mb-1 ml-1">
            Email Address
          </label>
          <input 
            type="email" 
            required 
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full h-12 p-4 rounded-xl border border-slate-100 bg-slate-50 text-slate-900 placeholder:text-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all"
            placeholder="email@example.com"
          />
        </div>
        
        <div>
          <label className="block text-[10px] font-black uppercase tracking-widest text-slate-400 mb-1 ml-1">
            Password
          </label>
          <input 
            type="password" 
            required 
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full h-12 p-4 rounded-xl border border-slate-100 bg-slate-50 text-slate-900 placeholder:text-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all"
            placeholder="••••••••"
          />
        </div>

        <button 
          type="submit" 
          disabled={loading}
          className="w-full h-12 mt-4 bg-[#00176B] text-white rounded-xl font-bold uppercase tracking-widest text-sm hover:bg-blue-900 shadow-lg active:scale-[0.98] transition-all disabled:opacity-50"
        >
          {loading ? "Processing..." : mode === "login" ? "Sign In" : "Sign Up Now"}
        </button>
      </form>
    </div>
  );
}