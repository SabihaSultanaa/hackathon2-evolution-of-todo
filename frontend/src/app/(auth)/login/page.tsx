"use client";

import Link from "next/link";
import { Rocket } from "lucide-react";
import { AuthForm } from "@/components/auth/auth-form";

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-[rgb(0,23,107)] flex items-center justify-center p-4 lg:p-6 relative overflow-hidden">
      
      {/* 1. BACKGROUND DECOR */}
      <div className="absolute inset-0 z-0 pointer-events-none select-none">
        <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-blue-400/10 blur-[120px] rounded-full" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-indigo-500/10 blur-[120px] rounded-full" />
      </div>

      {/* 2. THE WHITE UNDERGLOW (The "Shade" behind the card) */}
      <div className="absolute w-full max-w-5xl h-[550px] bg-white/10 blur-[100px] rounded-[2.5rem] pointer-events-none" />

      {/* 3. THE MAIN 3D CARD */}
      <div className="relative z-10 w-full max-w-5xl bg-white rounded-[3rem] 
        shadow-[0_50px_100px_-20px_rgba(0,0,0,0.6),0_0_50px_rgba(255,255,255,0.1),inset_0_1px_1px_rgba(255,255,255,0.5)] 
        flex flex-col lg:flex-row overflow-hidden min-h-[600px]">
        
        {/* LEFT SIDE: Brand Panel (Navy Blue Gradient) */}
        <div className="w-full lg:w-[45%] bg-gradient-to-br from-[rgb(0,35,140)] to-[rgb(0,23,107)] p-8 lg:p-12 flex flex-col relative">
          {/* Subtle Shine */}
          <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-white/5 to-transparent pointer-events-none" />
          
          <div className="relative z-20 h-full flex flex-col">
            <div className="flex items-center gap-2 mb-10">
              <Rocket className="text-white h-6 w-6" />
              <span className="text-white font-black tracking-widest uppercase text-xl">Designixer</span>
            </div>

            <div className="space-y-6">
              <div className="inline-block bg-white/10 px-4 py-1 rounded-lg border border-white/10">
                <span className="text-white font-bold text-xs tracking-widest uppercase">Welcome Back</span>
              </div>
              <h2 className="text-4xl font-black text-white leading-tight uppercase tracking-tighter drop-shadow-lg">
                Ready to crush <br /> your goals?
              </h2>
              <p className="text-blue-100/70 text-sm max-w-[280px] leading-relaxed">
                Log in to sync your tasks and continue your journey to peak productivity.
              </p>
            </div>

            {/* CRYSTAL CLEAR ROCKET */}
            <div className="mt-auto pt-6 flex justify-center lg:justify-start">
               <div className="animate-bounce duration-[4000ms]">
                  <Rocket 
                    className="h-32 w-32 text-white drop-shadow-[0_20px_40px_rgba(0,0,0,0.6)] rotate-[15deg]" 
                    strokeWidth={1.5}
                  />
               </div>
            </div>
          </div>
        </div>

        {/* RIGHT SIDE: White Panel */}
        <div className="w-full lg:w-[55%] bg-slate-50/50 p-8 lg:p-12 flex flex-col justify-center items-center relative z-20">
          
          {/* FORM CARD: This adds a "Card-on-Card" effect to fill the space beautifully */}
          <div className="w-full max-w-sm bg-white p-8 rounded-[2rem] shadow-[0_20px_40px_rgba(0,0,0,0.05)] border border-slate-100 relative z-30">
            <div className="text-center mb-8">
               <h1 className="text-3xl font-black text-[rgb(0,23,107)] uppercase tracking-tighter">Log In</h1>
               <p className="text-slate-400 text-[10px] font-bold uppercase tracking-widest mt-1">Access your dashboard</p>
            </div>

            {/* THE FORM */}
            <div className="relative text-slate-900 pointer-events-auto">
               <AuthForm mode="login" />
            </div>

            <div className="mt-8 text-center">
              <p className="text-slate-500 text-[10px] font-bold uppercase tracking-widest">
                Don't have an account?{" "}
                <Link href="/register" className="text-[rgb(0,23,107)] font-black hover:underline underline-offset-4 decoration-2 cursor-pointer ml-1">
                  Sign Up
                </Link>
              </p>
            </div>
          </div>

          {/* Bottom Branding / Links */}
          <div className="mt-8 flex gap-6 text-[10px] font-bold text-slate-300 uppercase tracking-widest">
            <span className="hover:text-[rgb(0,23,107)] cursor-pointer transition-colors">Privacy Policy</span>
            <span>•</span>
            <span className="hover:text-[rgb(0,23,107)] cursor-pointer transition-colors">Terms of Service</span>
          </div>
        </div>
      </div>
    </div>
  );
}