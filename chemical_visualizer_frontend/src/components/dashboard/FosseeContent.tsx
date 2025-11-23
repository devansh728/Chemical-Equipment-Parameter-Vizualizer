import { motion } from 'framer-motion';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { 
  FlaskConical, 
  Activity, 
  BarChart3, 
  Zap, 
  Bell, 
  FileDown, 
  Lock, 
  Sparkles,
  Upload,
  Layers,
  Database,
  Radio
} from 'lucide-react';

const features = [
  {
    icon: Activity,
    title: 'Instant CSV Analysis',
    description: 'Pandas-powered backend analyzes your equipment data in seconds',
    color: 'text-blue-500'
  },
  {
    icon: BarChart3,
    title: 'Dynamic 2D Visualizations',
    description: 'Interactive Bar, Doughnut, and Scatter plots with Chart.js',
    color: 'text-purple-500'
  },
  {
    icon: Zap,
    title: 'Asynchronous Processing',
    description: 'Celery task queue handles large files without freezing the UI',
    color: 'text-yellow-500'
  },
  {
    icon: Bell,
    title: 'Real-time Updates',
    description: 'WebSocket notifications when your analysis is complete',
    color: 'text-green-500'
  },
  {
    icon: FileDown,
    title: 'PDF Report Generation',
    description: 'Download professional, print-ready reports with one click',
    color: 'text-red-500'
  },
  {
    icon: Lock,
    title: 'Secure & Persistent',
    description: 'JWT authentication with personal history of your last 5 uploads',
    color: 'text-indigo-500'
  },
  {
    icon: Sparkles,
    title: 'Animated UI',
    description: 'Fluid interface built with Framer Motion and Shadcn/ui',
    color: 'text-pink-500'
  },
  {
    icon: FlaskConical,
    title: 'DWSIM Integration',
    description: 'Perfect post-processor for DWSIM simulation CSV exports',
    color: 'text-cyan-500'
  }
];

const techStack = [
  {
    icon: Layers,
    title: 'Frontend',
    tech: 'React • Vite • TypeScript • Chart.js • Framer Motion • TailwindCSS',
    color: 'border-blue-500/50'
  },
  {
    icon: Database,
    title: 'Backend',
    tech: 'Django • REST Framework • Python • Pandas',
    color: 'border-green-500/50'
  },
  {
    icon: Zap,
    title: 'Async & Real-time',
    tech: 'Celery • Redis • Django Channels • WebSockets',
    color: 'border-yellow-500/50'
  },
  {
    icon: Radio,
    title: 'DevOps',
    tech: 'Docker • Docker Compose • SQLite',
    color: 'border-purple-500/50'
  }
];

export const FosseeContent = () => {
  return (
    <div className="space-y-8 pb-8">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center space-y-4 py-8"
      >
        <div className="flex items-center justify-center gap-3 mb-4">
          <FlaskConical className="w-12 h-12 text-primary" />
          <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            FOSSEE Chemical Equipment Visualizer
          </h1>
        </div>
        
        <p className="text-lg md:text-xl text-muted-foreground max-w-3xl mx-auto">
          Transform DWSIM simulation data into actionable insights with real-time analysis
        </p>
        
        <p className="text-sm text-muted-foreground max-w-2xl mx-auto">
          A high-performance tool designed to bridge the gap between raw chemical process data and actionable insights. 
          Upload your equipment parameters and instantly see comprehensive summaries, dynamic charts, and detailed reports.
        </p>
        
        <div className="flex items-center justify-center gap-4 pt-4">
          <Button size="lg" className="gap-2">
            <Upload className="w-4 h-4" />
            Upload CSV to Begin
          </Button>
          <Button size="lg" variant="outline">
            Learn More
          </Button>
        </div>
      </motion.div>

      {/* FOSSEE & DWSIM Context */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
      >
        <Card className="bg-card/80 backdrop-blur-sm border-border/50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FlaskConical className="w-5 h-5" />
              About FOSSEE & DWSIM
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4 text-sm text-muted-foreground">
            <div>
              <h4 className="font-semibold text-foreground mb-2">What is FOSSEE?</h4>
              <p>
                FOSSEE (Free and Open Source Software for Education) is an initiative at IIT Bombay that promotes 
                the use of FOSS in academia and research. It aims to reduce dependency on proprietary software, 
                build a community around open-source tools, and enhance the quality of education.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-foreground mb-2">What is DWSIM?</h4>
              <p>
                DWSIM is an open-source, CAPE-OPEN compliant chemical process simulator. Engineers use DWSIM to 
                model complex chemical plants, run simulations of thermodynamic processes, and analyze the results.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-foreground mb-2">How This Tool Fits In</h4>
              <p>
                This application acts as a fast, web-based post-processor for DWSIM. Run a simulation in DWSIM, 
                export the equipment parameters as a CSV, and upload it here for instant visualization, insight, 
                and reporting. It makes the powerful data from DWSIM more accessible, interactive, and easier to share.
              </p>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Features Grid */}
      <div className="space-y-4">
        <motion.h2
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="text-2xl font-bold text-foreground"
        >
          Core Features
        </motion.h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.2 + index * 0.05 }}
            >
              <Card className="bg-card/80 backdrop-blur-sm border-border/50 h-full hover:border-primary/50 transition-colors">
                <CardHeader>
                  <feature.icon className={`w-8 h-8 ${feature.color} mb-2`} />
                  <CardTitle className="text-base">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-xs">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Tech Stack */}
      <div className="space-y-4">
        <motion.h2
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="text-2xl font-bold text-foreground"
        >
          Technology Stack
        </motion.h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {techStack.map((stack, index) => (
            <motion.div
              key={stack.title}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.4, delay: 0.4 + index * 0.1 }}
            >
              <Card className={`bg-card/80 backdrop-blur-sm border-2 ${stack.color}`}>
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-2">
                    <stack.icon className="w-5 h-5" />
                    {stack.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-xs text-muted-foreground">{stack.tech}</p>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Architecture Overview */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.6 }}
      >
        <Card className="bg-card/80 backdrop-blur-sm border-border/50">
          <CardHeader>
            <CardTitle>Application Architecture</CardTitle>
            <CardDescription>Modern, decoupled architecture for performance and scalability</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3 text-sm text-muted-foreground">
            <div className="flex items-start gap-3">
              <div className="w-2 h-2 rounded-full bg-blue-500 mt-2" />
              <div>
                <span className="font-semibold text-foreground">Frontend (React + Vite):</span> Responsive SPA 
                with Shadcn/ui, Chart.js for visualizations, and Framer Motion for animations
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-2 h-2 rounded-full bg-green-500 mt-2" />
              <div>
                <span className="font-semibold text-foreground">Backend (Django + DRF):</span> RESTful API 
                with JWT authentication and comprehensive business logic
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-2 h-2 rounded-full bg-yellow-500 mt-2" />
              <div>
                <span className="font-semibold text-foreground">Async Task Queue (Celery + Redis):</span> Background 
                workers perform heavy Pandas analysis without blocking the UI
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-2 h-2 rounded-full bg-purple-500 mt-2" />
              <div>
                <span className="font-semibold text-foreground">Real-time (Django Channels):</span> WebSocket 
                server pushes instant notifications when analysis completes
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Call to Action */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
        className="text-center py-8"
      >
        <p className="text-muted-foreground mb-4">
          Ready to analyze your chemical equipment data?
        </p>
        <p className="text-sm text-muted-foreground">
          Upload a CSV file or select a dataset from your history to get started
        </p>
      </motion.div>
    </div>
  );
};
