import React, { useState } from 'react';
import { 
  LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer, 
  ScatterChart, Scatter, ZAxis, BarChart, Bar, Cell, PieChart, Pie 
} from 'recharts';
import { 
  TrendingUp, AlertTriangle, Users, Target, ArrowRight, BrainCircuit, 
  ShieldAlert, Activity, CheckCircle2, DollarSign, Layout, Menu, X,
  Briefcase, Scale, Globe, Lightbulb
} from 'lucide-react';

// --- DATA ENGINE (NORMALIZED) ---

const HEADCOUNT_TREND = [
  { date: 'Mar 22', Internal: 419, Agency: 18, Deel: 4, Total: 442 },
  { date: 'Sep 22', Internal: 522, Agency: 44, Deel: 2, Total: 569 },
  { date: 'Mar 23', Internal: 566, Agency: 22, Deel: 15, Total: 604 },
  { date: 'Sep 23', Internal: 588, Agency: 36, Deel: 25, Total: 650 },
  { date: 'Jun 24', Internal: 650, Agency: 50, Deel: 35, Total: 739 },
  { date: 'Apr 25', Internal: 707, Agency: 64, Deel: 33, Total: 812 },
  { date: 'Oct 25', Internal: 769, Agency: 90, Deel: 67, Total: 941 },
  { date: 'Jan 26', Internal: 684, Agency: 53, Deel: 50, Total: 787 }, // Rightsizing Event
];

const RISK_MATRIX = [
  { name: 'Customer Service', investment: 11382, voluntary: 29, dismissal: 51, totalExits: 80, headcount: 145, risk: 'Critical', color: '#e9437c' },
  { name: 'Product', investment: 10081, voluntary: 12, dismissal: 25, totalExits: 37, headcount: 85, risk: 'High', color: '#f7b53e' },
  { name: 'Tech & IT', investment: 29500, voluntary: 8, dismissal: 20, totalExits: 28, headcount: 230, risk: 'Stable', color: '#44de97' },
  { name: 'Data & BI', investment: 6213, voluntary: 2, dismissal: 5, totalExits: 7, headcount: 45, risk: 'Medium', color: '#a37dff' },
  { name: 'Marketing', investment: 6855, voluntary: 4, dismissal: 2, totalExits: 6, headcount: 55, risk: 'Medium', color: '#a37dff' },
];

const EXIT_TYPE_DATA = [
  { name: 'Voluntary', value: 55, color: '#a37dff' }, 
  { name: 'Involuntary (Dismissal)', value: 103, color: '#e9437c' } 
];

const KPIS = {
  headcount: 787,
  growth: '-16%',
  dismissalRate: '18.2%',
  nps: 11.76
};

// --- BRAND CONSTANTS ---
const COLORS = {
  pink: '#e9437c',
  purple: '#a37dff',
  green: '#44de97',
  blue: '#4285f4',
  yellow: '#f7b53e',
  textMain: '#1e293b',
  textMuted: '#64748b'
};

// --- COMPONENT LIBRARY ---

const Card = ({ children, className = "", noPadding = false }) => (
  <div className={`bg-white rounded-xl border border-slate-100 shadow-sm ${noPadding ? '' : 'p-6'} ${className}`}>
    {children}
  </div>
);

const InsightBadge = ({ type, text }) => {
  const styles = {
    critical: { bg: 'bg-red-50', text: 'text-[#e9437c]', border: 'border-red-100' },
    warning: { bg: 'bg-amber-50', text: 'text-[#f7b53e]', border: 'border-amber-100' },
    success: { bg: 'bg-emerald-50', text: 'text-[#44de97]', border: 'border-emerald-100' },
    info: { bg: 'bg-blue-50', text: 'text-[#4285f4]', border: 'border-blue-100' }
  };
  const style = styles[type] || styles.info;
  
  return (
    <div className={`flex items-start gap-2 p-3 rounded-lg border text-sm ${style.bg} ${style.text} ${style.border}`}>
      <BrainCircuit size={16} className="mt-0.5 shrink-0" />
      <span>{text}</span>
    </div>
  );
};

// --- SECTIONS ---

const ExecutiveSummary = () => (
  <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
    <div className="bg-gradient-to-br from-[#4285f4] to-[#a37dff] text-white p-6 rounded-xl md:col-span-1 shadow-lg">
      <div className="text-blue-100 text-xs font-bold uppercase tracking-widest mb-2">Total Active</div>
      <div className="text-4xl font-bold mb-1">{KPIS.headcount}</div>
      <div className="flex items-center text-[#e9437c] text-sm font-medium bg-white/10 w-fit px-2 py-1 rounded">
        <TrendingUp size={16} className="mr-1" /> {KPIS.growth} (Rightsized)
      </div>
    </div>
    
    <Card className="md:col-span-3 flex flex-col justify-center border-l-4" style={{ borderLeftColor: COLORS.pink }}>
      <div className="flex items-center gap-2 mb-2">
        <ShieldAlert style={{ color: COLORS.pink }} size={20} />
        <h3 className="font-bold text-slate-800">Strategic Correction: Stability Achieved (941 → 787)</h3>
      </div>
      <p className="text-slate-600 text-sm">
        Following the unorganized scaling of 2025, we have successfully rightsized the organization by <strong>-16%</strong> (primarily Agency reduction).
        The focus for 2026 is now strictly on <strong>Quality of Hire</strong> and stabilizing the core "Deel" & Internal teams.
      </p>
    </Card>
  </div>
);

const SoWhatSection = () => (
  <div className="mb-10">
    <div className="flex items-center gap-2 mb-4">
      <Target style={{ color: COLORS.blue }} />
      <h2 className="text-xl font-bold text-slate-900">Executive Briefing: The "So What?"</h2>
    </div>
    
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      
      {/* 1. STRATEGY - The Correction */}
      <div className="relative group hover:-translate-y-1 transition-transform duration-200">
        <Card className="relative h-full border-t-4 flex flex-col" style={{ borderTopColor: COLORS.blue }}>
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-blue-50 rounded-lg" style={{ color: COLORS.blue }}><Scale size={20}/></div>
            <h3 className="font-bold text-slate-800">The Scaling Correction</h3>
          </div>
          <p className="text-sm text-slate-600 mb-4 flex-grow">
            <strong>Insight:</strong> We have corrected the 2025 over-hiring (peak 941) down to <strong>787</strong>. The surge was a reactive response to ambitious targets without structural readiness.
          </p>
          <div className="pt-4 border-t border-slate-100">
            <strong className="text-xs font-bold uppercase" style={{ color: COLORS.textMain }}>Recommendation:</strong>
            <p className="text-xs text-slate-500 mt-1">Formalize Q1 Headcount Planning linked strictly to the new CFO's revenue forecasts. No req approval without P&L justification.</p>
          </div>
        </Card>
      </div>

      {/* 2. QUALITY - The False Positives */}
      <div className="relative group hover:-translate-y-1 transition-transform duration-200">
        <Card className="relative h-full border-t-4 flex flex-col" style={{ borderTopColor: COLORS.pink }}>
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-red-50 rounded-lg" style={{ color: COLORS.pink }}><Activity size={20}/></div>
            <h3 className="font-bold text-slate-800">The "False Positive" Cost</h3>
          </div>
          <p className="text-sm text-slate-600 mb-4 flex-grow">
            <strong>Insight:</strong> 59 "Disciplinary" exits are actually performance failures. Our current assessments are ineffective, leading to "False Positive" hires.
          </p>
          <div className="pt-4 border-t border-slate-100">
            <div className="flex justify-between items-center">
              <strong className="text-xs font-bold uppercase" style={{ color: COLORS.textMain }}>Recommendation:</strong>
              <span className="text-[10px] text-slate-400 italic">*Est. based on market data</span>
            </div>
            <p className="text-xs text-slate-500 mt-1">Replace subjective screening with objective technical assessments. Cap hiring volume to ensure quality validation.</p>
          </div>
        </Card>
      </div>

      {/* 3. FINANCE - The Training Leak */}
      <div className="relative group hover:-translate-y-1 transition-transform duration-200">
        <Card className="relative h-full border-t-4 flex flex-col" style={{ borderTopColor: COLORS.yellow }}>
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-amber-50 rounded-lg" style={{ color: COLORS.yellow }}><DollarSign size={20}/></div>
            <h3 className="font-bold text-slate-800">The Governance Gap</h3>
          </div>
          <p className="text-sm text-slate-600 mb-4 flex-grow">
            <strong>Insight:</strong> Lack of budgeting governance led to loose training spend (€87k). CS invests heavily in probationers who are subsequently fired for performance.
          </p>
          <div className="pt-4 border-t border-slate-100">
            <strong className="text-xs font-bold uppercase" style={{ color: COLORS.textMain }}>Recommendation:</strong>
            <p className="text-xs text-slate-500 mt-1">Centralize training budget under HR. Freeze external training for employees with &lt;6 months tenure until quality filter is fixed.</p>
          </div>
        </Card>
      </div>

      {/* 4. LEADERSHIP - The "Accidental" Managers */}
      <div className="relative group hover:-translate-y-1 transition-transform duration-200">
        <Card className="relative h-full border-t-4 flex flex-col" style={{ borderTopColor: COLORS.purple }}>
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-purple-50 rounded-lg" style={{ color: COLORS.purple }}><Briefcase size={20}/></div>
            <h3 className="font-bold text-slate-800">Delivery vs. Development</h3>
          </div>
          <p className="text-sm text-slate-600 mb-4 flex-grow">
            <strong>Insight:</strong> Culture prioritizes delivery over talent retention. Long-time employees were promoted on tenure without leadership assessment ("Peter Principle" risk).
          </p>
          <div className="pt-4 border-t border-slate-100">
            <strong className="text-xs font-bold uppercase" style={{ color: COLORS.textMain }}>Recommendation:</strong>
            <p className="text-xs text-slate-500 mt-1">Audit all Team Leads with &gt;2 years tenure. Launch "Manager Fundamentals" to shift focus from output to team effectiveness.</p>
          </div>
        </Card>
      </div>

      {/* 5. STRUCTURE - The Deel Disconnect */}
      <div className="relative group hover:-translate-y-1 transition-transform duration-200">
        <Card className="relative h-full border-t-4 flex flex-col" style={{ borderTopColor: COLORS.blue }}>
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-blue-50 rounded-lg" style={{ color: COLORS.blue }}><Globe size={20}/></div>
            <h3 className="font-bold text-slate-800">The "Partner" Illusion</h3>
          </div>
          <p className="text-sm text-slate-600 mb-4 flex-grow">
            <strong>Insight:</strong> Deel staff are effectively internal employees located abroad, yet churn at ~40%. Treating them as "external partners" is damaging retention.
          </p>
          <div className="pt-4 border-t border-slate-100">
            <strong className="text-xs font-bold uppercase" style={{ color: COLORS.textMain }}>Recommendation:</strong>
            <p className="text-xs text-slate-500 mt-1">Harmonize onboarding and feedback loops. Treat Deel staff as FTEs for all culture and performance programs.</p>
          </div>
        </Card>
      </div>

      {/* 6. CULTURE - The Vision Gap */}
      <div className="relative group hover:-translate-y-1 transition-transform duration-200">
        <Card className="relative h-full border-t-4 flex flex-col" style={{ borderTopColor: COLORS.green }}>
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-emerald-50 rounded-lg" style={{ color: COLORS.green }}><Lightbulb size={20}/></div>
            <h3 className="font-bold text-slate-800">Quantity vs. Quality</h3>
          </div>
          <p className="text-sm text-slate-600 mb-4 flex-grow">
            <strong>Insight:</strong> The focus on delivery volume has overshadowed efficient retention. High churn in Product/IT (mixed levels) signals burnout and lack of strategic direction.
          </p>
          <div className="pt-4 border-t border-slate-100">
            <strong className="text-xs font-bold uppercase" style={{ color: COLORS.textMain }}>Recommendation:</strong>
            <p className="text-xs text-slate-500 mt-1">Executive roadshows to clarify 2026 Strategy. Shift performance measurement from "Output Volume" to "Strategic Impact".</p>
          </div>
        </Card>
      </div>

    </div>
  </div>
);

const GrowthTab = () => (
  <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
    <Card className="lg:col-span-2">
      <div className="flex justify-between items-center mb-6">
        <h3 className="font-bold text-lg text-slate-800">Workforce Velocity (2022-2026)</h3>
        <span className="px-3 py-1 bg-emerald-50 rounded-full text-xs font-bold" style={{ color: COLORS.green }}>Correction Phase</span>
      </div>
      <div className="h-80 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={HEADCOUNT_TREND} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="colorInt" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={COLORS.blue} stopOpacity={0.1}/>
                <stop offset="95%" stopColor={COLORS.blue} stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
            <XAxis dataKey="date" axisLine={false} tickLine={false} tick={{fill: COLORS.textMuted, fontSize: 12}} dy={10} />
            <YAxis axisLine={false} tickLine={false} tick={{fill: COLORS.textMuted, fontSize: 12}} />
            <RechartsTooltip 
              contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
            />
            <Legend />
            <Area type="monotone" dataKey="Internal" name="FTEs (Internal)" stroke={COLORS.blue} strokeWidth={3} fill="url(#colorInt)" />
            <Area type="monotone" dataKey="Agency" name="Contingent (Agency)" stroke={COLORS.yellow} strokeWidth={2} fillOpacity={0} />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </Card>

    <div className="space-y-6">
      <Card>
        <h3 className="font-bold text-slate-800 mb-4">Exit Composition (2025)</h3>
        <div className="h-48 w-full relative">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={EXIT_TYPE_DATA}
                innerRadius={60}
                outerRadius={80}
                paddingAngle={5}
                dataKey="value"
              >
                {EXIT_TYPE_DATA.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <RechartsTooltip />
            </PieChart>
          </ResponsiveContainer>
          <div className="absolute inset-0 flex items-center justify-center flex-col pointer-events-none">
            <span className="text-3xl font-bold text-slate-800">65%</span>
            <span className="text-xs text-slate-500 uppercase">Involuntary</span>
          </div>
        </div>
        <div className="flex justify-center gap-4 text-xs mt-2">
          <div className="flex items-center gap-1"><div className="w-2 h-2 rounded-full" style={{ backgroundColor: COLORS.purple }}></div>Voluntary</div>
          <div className="flex items-center gap-1"><div className="w-2 h-2 rounded-full" style={{ backgroundColor: COLORS.pink }}></div>Dismissal</div>
        </div>
      </Card>
      
      <InsightBadge type="success" text="Workforce successfully stabilized at 787. Agency dependency reduced from 90 to 53." />
    </div>
  </div>
);

const RiskTab = () => (
  <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
    <Card className="lg:col-span-2">
      <div className="mb-6">
        <h3 className="font-bold text-lg text-slate-800">The Efficiency Matrix (2025 Analysis)</h3>
        <p className="text-slate-500 text-sm">Correlating Training Investment (X) vs. Total Exits (Y)</p>
      </div>
      <div className="h-96 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" dataKey="investment" name="Investment" unit="€" stroke="#94a3b8" />
            <YAxis type="number" dataKey="totalExits" name="Total Exits" stroke="#94a3b8" />
            <ZAxis type="number" dataKey="headcount" range={[400, 4000]} />
            <RechartsTooltip 
              cursor={{ strokeDasharray: '3 3' }}
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  const d = payload[0].payload;
                  return (
                    <div className="bg-slate-900 text-white p-3 rounded-lg text-sm shadow-xl">
                      <p className="font-bold mb-1" style={{ color: COLORS.green }}>{d.name}</p>
                      <div className="grid grid-cols-2 gap-x-4 gap-y-1">
                        <span className="text-slate-400">Spend:</span>
                        <span>€{d.investment.toLocaleString()}</span>
                        <span className="text-slate-400">Dismissals:</span>
                        <span style={{ color: COLORS.pink }}>{d.dismissal}</span>
                        <span className="text-slate-400">Voluntary:</span>
                        <span>{d.voluntary}</span>
                      </div>
                    </div>
                  );
                }
                return null;
              }}
            />
            <Scatter name="Departments" data={RISK_MATRIX}>
              {RISK_MATRIX.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Scatter>
          </ScatterChart>
        </ResponsiveContainer>
      </div>
    </Card>

    <div className="space-y-4">
      <h3 className="font-bold text-slate-800">Risk Diagnosis</h3>
      
      <div className="p-4 bg-red-50 border border-red-100 rounded-xl">
        <div className="flex justify-between items-center mb-2">
          <strong className="text-red-900">Customer Service</strong>
          <span className="bg-white/50 border border-red-100 text-red-700 text-xs px-2 py-1 rounded-full font-bold">CRITICAL</span>
        </div>
        <p className="text-sm text-red-800 mb-3">
          Highest churn volume (80 exits) despite high training spend (€11k). 
        </p>
        <div className="text-xs font-mono bg-white p-2 rounded text-red-900 border border-red-100">
          Ratio: 1 Dismissal per €223 spent
        </div>
      </div>

      <div className="p-4 bg-emerald-50 border border-emerald-100 rounded-xl">
        <div className="flex justify-between items-center mb-2">
          <strong className="text-emerald-900">Tech & IT</strong>
          <span className="bg-white/50 border border-emerald-100 text-emerald-700 text-xs px-2 py-1 rounded-full font-bold">STABLE</span>
        </div>
        <p className="text-sm text-emerald-800 mb-3">
          High investment (€29k) correlates with lower relative churn.
        </p>
        <div className="text-xs font-mono bg-white p-2 rounded text-emerald-900 border border-emerald-100">
          Ratio: 1 Dismissal per €1,475 spent
        </div>
      </div>

      <div className="p-4 bg-white border border-slate-200 rounded-xl">
        <strong className="text-slate-800 block mb-1">Product</strong>
        <p className="text-sm text-slate-500">
          High "Regrettable" turnover (12 voluntary). Exit interviews cite "Lack of Strategic Vision."
        </p>
      </div>
    </div>
  </div>
);

// --- MAIN APP SHELL ---

export default function TalentStrategyApp() {
  const [activeTab, setActiveTab] = useState('strategy');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const tabs = [
    { id: 'strategy', label: 'Executive Briefing', icon: Target },
    { id: 'growth', label: 'Growth & Velocity', icon: TrendingUp },
    { id: 'risk', label: 'Efficiency & Risk', icon: ShieldAlert },
  ];

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 pb-20" style={{ fontFamily: "'Roboto', sans-serif" }}>
      {/* Font Injection */}
      <style>
        {`@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');`}
      </style>

      {/* Navigation */}
      <nav className="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-20">
            <div className="flex items-center gap-3">
              <img 
                src="https://media.licdn.com/dms/image/v2/C4E0BAQGm6GIMqyYrbg/company-logo_200_200/company-logo_200_200/0/1656910905863/leadtech_group_logo?e=1770854400&v=beta&t=O6E2jtBpxrtCZWGFAQArQQkkipK_4MDLAUyEZftIGrY" 
                alt="Leadtech Logo" 
                className="h-12 w-12 rounded-lg"
              />
              <span className="font-bold text-xl tracking-tight text-slate-900">Talent<span style={{ color: COLORS.blue }}>Intel</span></span>
            </div>
            
            {/* Desktop Nav */}
            <div className="hidden md:flex space-x-8">
              {tabs.map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors ${
                    activeTab === tab.id
                      ? 'text-slate-900'
                      : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
                  }`}
                  style={{ borderColor: activeTab === tab.id ? COLORS.pink : 'transparent' }}
                >
                  <tab.icon size={16} className="mr-2" style={{ color: activeTab === tab.id ? COLORS.pink : 'currentColor' }} />
                  {tab.label}
                </button>
              ))}
            </div>

            {/* Mobile Menu Button */}
            <div className="flex items-center md:hidden">
              <button onClick={() => setMobileMenuOpen(!mobileMenuOpen)} className="text-slate-500">
                {mobileMenuOpen ? <X /> : <Menu />}
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-slate-900">2025 Workforce Intelligence Review</h1>
          <p className="text-slate-500">Strategic analysis of H1-H2 2025 performance data.</p>
        </div>

        {/* Global KPI Summary */}
        <ExecutiveSummary />

        {/* Tab Content */}
        {activeTab === 'strategy' && (
          <div className="animate-in fade-in duration-500">
            <SoWhatSection />
            
            <div className="rounded-2xl p-8 text-white relative overflow-hidden shadow-xl" style={{ backgroundColor: '#1e293b' }}>
              <div className="relative z-10 flex flex-col md:flex-row items-center justify-between gap-6">
                <div>
                  <h3 className="text-2xl font-bold mb-2">Ready to act?</h3>
                  <p className="text-slate-300 max-w-xl">
                    The data suggests that <strong>slowing down</strong> hiring velocity to fix the quality filter will actually <strong>accelerate</strong> net productive headcount in 2026.
                  </p>
                </div>
                <button 
                  className="px-6 py-3 rounded-lg font-bold transition-transform hover:scale-105 shadow-lg text-white border border-white/20"
                  style={{ backgroundColor: COLORS.pink }}
                >
                  Approve Q1 Plan
                </button>
              </div>
              {/* Background Decoration */}
              <div className="absolute top-0 right-0 -mr-20 -mt-20 w-64 h-64 rounded-full mix-blend-screen filter blur-3xl opacity-20 animate-blob" style={{ backgroundColor: COLORS.blue }}></div>
              <div className="absolute bottom-0 left-0 -ml-20 -mb-20 w-64 h-64 rounded-full mix-blend-screen filter blur-3xl opacity-20 animate-blob animation-delay-2000" style={{ backgroundColor: COLORS.pink }}></div>
            </div>
          </div>
        )}

        {activeTab === 'growth' && <GrowthTab />}
        
        {activeTab === 'risk' && <RiskTab />}

      </main>
    </div>
  );
}