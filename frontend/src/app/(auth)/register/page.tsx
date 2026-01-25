"use client"

import Link from "next/link"
import { User, Mail, Lock, Rocket, ListTodo, Target, Zap } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { AuthForm } from "@/components/auth/auth-form"

export default function RegisterPage() {
  return (
    <div className="min-h-screen bg-[rgb(0,23,107)] flex items-center justify-center p-4 lg:p-6 relative overflow-hidden">
      
      {/* Background Decor */}
      <div className="absolute inset-0 pointer-events-none select-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-cyan-400/10 blur-[120px] rounded-full" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-400/10 blur-[120px] rounded-full" />
      </div>

      {/* 3D FLOATING CARD: We use a heavy shadow and a subtle top-light ring */}
      <div className="relative z-10 w-full max-w-5xl bg-white rounded-[2.5rem] 
        shadow-[0_50px_100px_-20px_rgba(0,0,0,0.7),0_30px_60px_-30px_rgba(0,0,0,0.8),inset_0_1px_1px_rgba(255,255,255,0.3)] 
        flex flex-col lg:flex-row overflow-hidden min-h-[550px]">
        
        {/* LEFT SIDE: Brand Panel (Navy Blue) */}
        {/* We use a subtle gradient here to give the Navy side its own 3D depth */}
        <div className="w-full lg:w-[45%] bg-gradient-to-b from-[rgb(5,28,117)] to-[rgb(0,23,107)] p-8 lg:p-12 flex flex-col relative">
          
          {/* Subtle 3D Shine Effect on the Left Panel */}
          <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-white/5 to-transparent pointer-events-none" />

          <div className="relative z-20 h-full flex flex-col">
            <div className="flex items-center gap-2 mb-10">
              <Rocket className="text-white h-6 w-6" />
              <span className="text-white font-black tracking-widest uppercase text-xl">Designixer</span>
            </div>

            <div className="space-y-6">
              <div className="inline-block bg-white/10 backdrop-blur-md px-4 py-1 rounded-lg border border-white/10">
                <span className="text-white font-bold text-xs tracking-widest uppercase text-nowrap">Master Your Day</span>
              </div>
              <h2 className="text-4xl font-black text-white leading-tight uppercase tracking-tighter drop-shadow-lg">
                Organize Your <br /> Tasks & Goals
              </h2>
              
              <ul className="space-y-4 text-white/90 text-sm">
                <li className="flex items-center gap-3">
                  <div className="p-1 bg-white/10 rounded-md shadow-inner"><ListTodo className="h-4 w-4 text-cyan-300" /></div>
                  Manage unlimited daily tasks
                </li>
                <li className="flex items-center gap-3">
                  <div className="p-1 bg-white/10 rounded-md shadow-inner"><Target className="h-4 w-4 text-cyan-300" /></div>
                  Track your long-term productivity
                </li>
                <li className="flex items-center gap-3">
                  <div className="p-1 bg-white/10 rounded-md shadow-inner"><Zap className="h-4 w-4 text-cyan-300" /></div>
                  Boost efficiency with Dark Mode
                </li>
              </ul>
            </div>

            <div className="mt-auto pt-6 flex justify-center lg:justify-end">
               <div className="animate-bounce duration-[4000ms]">
                  <Rocket 
                    className="h-32 w-32 text-white drop-shadow-[0_20px_40px_rgba(0,0,0,0.8)] rotate-[15deg]" 
                    strokeWidth={1.5}
                  />
               </div>
            </div>
          </div>
        </div>

        {/* RIGHT SIDE: White Form Panel */}
        <div className="w-full lg:w-[55%] bg-white p-8 lg:p-12 flex flex-col justify-center items-center relative z-20">
          <div className="w-full max-w-sm space-y-6">
            <div className="text-center">
               <h1 className="text-3xl font-black text-[rgb(0,23,107)] uppercase tracking-tighter">Sign Up</h1>
               <p className="text-slate-400 text-xs font-bold uppercase tracking-widest mt-1">Join the community</p>
            </div>

            <div className="relative text-slate-900 pointer-events-auto">
               <AuthForm mode="register" />
            </div>

            <div className="space-y-4 pt-4">
              <p className="text-center text-slate-500 text-xs font-medium uppercase tracking-widest">
                Already member? <Link href="/login" className="text-[rgb(0,23,107)] font-black hover:underline underline-offset-4">Log In</Link>
              </p>

              <div className="flex justify-center gap-6">
   {/* Google Button */}
   <button className="p-4 border border-slate-100 rounded-2xl hover:bg-slate-50 transition-all shadow-sm hover:shadow-md hover:-translate-y-1 cursor-pointer bg-white group">
      <img 
        src="https://www.google.com/favicon.ico" 
        className="w-7 h-7 grayscale-[0.2] group-hover:grayscale-0 transition-all" 
        alt="Google" 
      />
   </button>
   
   {/* Facebook Button */}
   <button className="p-4 border border-slate-100 rounded-2xl hover:bg-slate-50 transition-all shadow-sm hover:shadow-md hover:-translate-y-1 cursor-pointer bg-white group">
      <img 
        src="https://www.facebook.com/favicon.ico" 
        className="w-7 h-7 grayscale-[0.2] group-hover:grayscale-0 transition-all" 
        alt="Facebook" 
      />
   </button>
</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}