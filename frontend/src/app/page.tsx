"use client"

import Link from "next/link"
import { CheckCircle2, Moon, Rocket } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function HomePage() {
  return (
    // FIXED: Added your specific theme color here to match the login/register pages
    <div className="min-h-screen flex flex-col overflow-x-hidden bg-[rgb(0,23,107)] relative">
      
      {/* 1. TOP BRANDING */}
      <header className="p-10 z-30"> {/* Increased z-index */}
        <div className="flex items-center gap-3">
          <h1 className="text-4xl font-black uppercase flex tracking-tighter">
            <span className="text-white">DESIG</span>
            <span 
              className="text-transparent ml-0.5" 
              style={{ WebkitTextStroke: '1.5px white' }}
            >
              NIXER
            </span>
          </h1>
        </div>
      </header>

      {/* 2. MAIN CONTENT AREA */}
      <main className="flex-1 flex flex-col lg:flex-row items-center px-10 lg:px-32 gap-12 z-20">
        
        {/* LEFT SIDE: Hero Text */}
        <div className="w-full lg:w-1/2 space-y-8 relative">
          <div className="space-y-4">
            <h1 className="text-6xl lg:text-7xl font-black text-white leading-tight tracking-tighter uppercase">
              The Ultimate <br />
              <span className="text-white">Task </span>
              <span 
                className="text-transparent" 
                style={{ WebkitTextStroke: '2px white' }}
              >
                Organizer
              </span>
            </h1>
            <p className="text-white text-lg max-w-lg leading-relaxed ">
              A simple, elegant way to organize your tasks, track your progress, and boost your daily productivity.
            </p>
          </div>

          <div className="flex items-center gap-8">
            {/* Added relative z-30 to button to ensure it is clickable */}
            <Button asChild className=" btn-adventure h-14 px-20 rounded-full text-lg font-bold text-white hover:bg-white/90 transition-all shadow-xl relative z-30">
              <Link href="/register">Get Started</Link>
            </Button> 
            
            <Link href="/login" className="underline text-white font-bold hover:text-cyan-400 transition-colors relative z-30">
              Sign In
            </Link>
          </div>
        </div>

        {/* RIGHT SIDE: Vertical Card Stack */}
        <div className="w-full lg:w-1/2 flex flex-col gap-5 lg:max-w-md ml-auto relative z-20">
          <FeatureCard 
            icon={<Rocket className="text-pink-500 h-8 w-8 " />}
            title="Create Tasks" 
            desc="Quickly add tasks with titles and descriptions."
            glowVariant="bg-blue-400/20"
          />
          
          <FeatureCard 
            icon={<CheckCircle2 className="text-yellow-500 h-8 w-8" />}
            title="Stay Organized" 
            desc="Mark tasks as complete and track progress." 
            glowVariant="bg-cyan-400/20"
          />
          
          <FeatureCard 
            icon={<Moon className="text-green-500 h-8 w-8" />}
            title="Dark Mode" 
            desc="Comfortable viewing for your eyes." 
            glowVariant="bg-indigo-400/20"
          />
        </div>
      </main>

      {/* BACKGROUND DECORATION (Behind everything) */}
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-cyan-500/10 blur-[120px] rounded-full pointer-events-none z-0" />
    </div>
  )
}

function FeatureCard({ icon, title, desc, glowVariant }: { icon: React.ReactNode, title: string, desc: string, glowVariant: string }) {
  return (
    <div className="group relative p-6 py-8 rounded-[2.5rem] bg-white/5 border border-white/10 backdrop-blur-xl transition-all duration-500 hover:bg-white/10 hover:border-cyan-300/50 hover:-translate-x-2 shadow-2xl flex items-center text-left gap-6 overflow-hidden">
      
      <div className={`absolute -top-10 -right-10 w-24 h-24 rounded-full blur-3xl opacity-30 ${glowVariant}`} />

      <div className="relative z-10 p-4 bg-white/5 rounded-2xl border border-white/10 group-hover:scale-110 group-hover:bg-cyan-400/20 transition-all duration-500 shrink-0">
        {icon}
      </div>
      
      <div className="space-y-1 relative z-10">
        <h3 className="text-lg font-black text-cyan-400 leading-tight uppercase group-hover:text-white transition-colors">
          {title}
        </h3>
        <p className="text-white/70 text-[11px] uppercase font-bold tracking-widest leading-relaxed">
          {desc}
        </p>
      </div>
    </div>
  )
}