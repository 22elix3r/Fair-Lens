import React from 'react';

interface EBIData {
  enterprise_bias_index: number;
  risk_tier: 'GREEN' | 'AMBER' | 'RED' | 'CRITICAL';
  risk_description: string;
  percentile_rank: number;
  dimensions: {
    metric_coverage: number;
    severity_weighted: number;
    temporal_stability: number;
    intersectional: number;
    remediation_velocity: number;
    regulatory_alignment: number;
  };
  biggest_risk_factor: string;
  improvement_priority: string[];
}

const TIER_COLORS = {
  GREEN:    { text: '#10a37f', bg: 'rgba(16,163,127,0.1)', border: '#10a37f' },
  AMBER:    { text: '#f59e0b', bg: 'rgba(245,158,11,0.1)',  border: '#f59e0b' },
  RED:      { text: '#ef4444', bg: 'rgba(239,68,68,0.1)',   border: '#ef4444' },
  CRITICAL: { text: '#ffb4ab', bg: 'rgba(147,0,10,0.3)',    border: '#93000a' },
};

const DIM_LABELS = {
  metric_coverage: 'Metric Coverage',
  severity_weighted: 'Severity Impact',
  temporal_stability: 'Temporal Stability',
  intersectional: 'Intersectional Coverage',
  remediation_velocity: 'Remediation Velocity',
  regulatory_alignment: 'Regulatory Alignment',
};

export function EBIWidget({ data }: { data: EBIData }) {
  const colors = TIER_COLORS[data.risk_tier] || TIER_COLORS.AMBER;
  const score = Math.round(data.enterprise_bias_index);
  
  // SVG circular gauge
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;
  
  return (
    <div className="bg-[#171717] border border-[#2f2f2f] rounded-xl p-6">
      
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-xl font-semibold text-white">Enterprise Bias Index</h3>
          <p className="text-sm text-[#b4b4b4] mt-1">
            Composite governance score — 6 weighted dimensions
          </p>
        </div>
        <span
          className="text-xs px-3 py-1 rounded-full border font-medium"
          style={{ color: colors.text, background: colors.bg, borderColor: colors.border }}
        >
          {data.risk_tier}
        </span>
      </div>
      
      {/* Two-column layout: gauge left, dims right */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* LEFT — Circular gauge */}
        <div className="flex flex-col items-center justify-center">
          <div className="relative">
            <svg width="140" height="140" viewBox="0 0 140 140">
              <circle
                cx="70" cy="70" r={radius}
                fill="none" stroke="#2f2f2f" strokeWidth="10"
              />
              <circle
                cx="70" cy="70" r={radius}
                fill="none"
                stroke={colors.text}
                strokeWidth="10"
                strokeDasharray={circumference}
                strokeDashoffset={strokeDashoffset}
                strokeLinecap="round"
                transform="rotate(-90 70 70)"
                style={{ transition: 'stroke-dashoffset 1s ease' }}
              />
              <text x="70" y="65" textAnchor="middle"
                fill="white" fontSize="28" fontWeight="600" dominantBaseline="middle"
              >{score}</text>
              <text x="70" y="90" textAnchor="middle"
                fill="#b4b4b4" fontSize="11"
              >/100</text>
            </svg>
          </div>
          
          <p className="text-sm text-[#b4b4b4] text-center mt-2">
            {data.risk_description}
          </p>
          <p className="text-xs mt-1" style={{ color: colors.text }}>
            Better than {Math.round(data.percentile_rank)}% of industry
          </p>
        </div>
        
        {/* RIGHT — 6 dimension bars */}
        <div className="space-y-3">
          {Object.entries(data.dimensions).map(([key, value]) => {
            const barColor = value >= 80 ? '#10a37f'
                           : value >= 60 ? '#f59e0b' : '#ef4444';
            return (
              <div key={key}>
                <div className="flex justify-between items-center mb-1">
                  <span className="text-xs text-[#b4b4b4]">
                    {DIM_LABELS[key as keyof typeof DIM_LABELS]}
                  </span>
                  <span className="text-xs font-medium"
                    style={{ color: barColor }}
                  >{Math.round(value)}</span>
                </div>
                <div className="h-1.5 bg-[#2f2f2f] rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-700"
                    style={{ width: `${value}%`, background: barColor }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>
      
      {/* Bottom — biggest risk + priorities */}
      <div className="mt-6 pt-4 border-t border-[#2f2f2f]">
        <div className="flex items-start gap-2 mb-3">
          <span className="material-symbols-outlined text-[16px] text-[#f59e0b] mt-0.5">
            warning
          </span>
          <div>
            <p className="text-[10px] text-[#b4b4b4] uppercase tracking-wider font-bold">
              Biggest Risk Factor
            </p>
            <p className="text-sm text-white mt-0.5">
              {data.biggest_risk_factor}
            </p>
          </div>
        </div>
        <div>
          <p className="text-[10px] text-[#b4b4b4] uppercase tracking-wider mb-2 font-bold">
            Improvement Priorities
          </p>
          {data.improvement_priority.map((p, i) => (
            <div key={i} className="flex items-center gap-2 mb-1">
              <span className="text-xs font-medium"
                style={{ color: '#10a37f' }}
              >{i + 1}.</span>
              <span className="text-sm text-[#b4b4b4]">{p}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
