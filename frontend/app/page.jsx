"use client";

import React, { useState, useEffect, useRef, useCallback } from 'react';
import Sidebar from '@/components/Sidebar';
import Topbar from '@/components/Topbar';
import PersonaPanel from '@/components/PersonaPanel';
import ChatPanel from '@/components/ChatPanel';
import OverviewPanel from '@/components/OverviewPanel';
import ReportModal from '@/components/ReportModal';
import ErrorToast from '@/components/ErrorToast';
import { INITIAL_DASHBOARD_DATA, THINKING_STEPS } from '@/lib/constants';

function generateSessionId() {
  return "session_" + Math.random().toString(36).substring(2, 11);
}

export default function DashboardPage() {
  const [dashboardData, setDashboardData] = useState(() => JSON.parse(JSON.stringify(INITIAL_DASHBOARD_DATA)));
  const [sessionId, setSessionId] = useState(generateSessionId);
  const [isDark, setIsDark] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isThinking, setIsThinking] = useState(false);
  const [thinkingStep, setThinkingStep] = useState(THINKING_STEPS[0]);
  const [errorMessage, setErrorMessage] = useState(null);
  const [isReportOpen, setIsReportOpen] = useState(false);
  const [timerSeconds, setTimerSeconds] = useState(0);

  const timerRef = useRef(null);
  const thinkingIntervalRef = useRef(null);

  // Determine API base URL
  const getApiUrl = useCallback(() => {
    if (process.env.NEXT_PUBLIC_API_URL) {
      return process.env.NEXT_PUBLIC_API_URL.replace(/\/+$/, '');
    }
    if (typeof window !== 'undefined') {
      const hostname = window.location.hostname;
      if (hostname === 'localhost' || hostname === '127.0.0.1') {
        return 'http://127.0.0.1:8001';
      }
    }
    return 'https://traceai-backend-rg.up.railway.app';
  }, []);

  // Timer logic
  useEffect(() => {
    timerRef.current = setInterval(() => {
      setTimerSeconds((prev) => prev + 1);
    }, 1000);

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  const formatTimer = () => {
    const min = String(Math.floor(timerSeconds / 60)).padStart(2, '0');
    const sec = String(timerSeconds % 60).padStart(2, '0');
    return `Running • ${min}:${sec}`;
  };

  // Dark mode effect
  const handleToggleDark = () => {
    setIsDark((prev) => {
      const next = !prev;
      if (typeof document !== 'undefined') {
        if (next) {
          document.body.classList.add('dark');
        } else {
          document.body.classList.remove('dark');
        }
      }
      return next;
    });
  };

  // Thinking step cycling
  useEffect(() => {
    if (isThinking) {
      let stepIdx = 0;
      setThinkingStep(THINKING_STEPS[0]);
      thinkingIntervalRef.current = setInterval(() => {
        stepIdx = (stepIdx + 1) % THINKING_STEPS.length;
        setThinkingStep(THINKING_STEPS[stepIdx]);
      }, 2000);
    } else {
      if (thinkingIntervalRef.current) {
        clearInterval(thinkingIntervalRef.current);
        thinkingIntervalRef.current = null;
      }
    }
    return () => {
      if (thinkingIntervalRef.current) clearInterval(thinkingIntervalRef.current);
    };
  }, [isThinking]);

  // Error toast auto-dismiss
  useEffect(() => {
    if (errorMessage) {
      const t = setTimeout(() => {
        setErrorMessage(null);
      }, 5000);
      return () => clearTimeout(t);
    }
  }, [errorMessage]);

  // Send message
  const handleSendMessage = async (message) => {
    if (!message || isLoading) return;

    setIsLoading(true);
    setIsThinking(true);
    setErrorMessage(null);

    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    // Optimistically add user message
    setDashboardData((prev) => {
      const newMessages = [
        ...prev.messages,
        {
          role: "scammer",
          sender: "Scammer",
          time: timeStr,
          content: message
        }
      ];
      return {
        ...prev,
        messages: newMessages
      };
    });

    try {
      const apiUrl = getApiUrl();
      const response = await fetch(`${apiUrl}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, session_id: sessionId })
      });

      if (!response.ok) {
        throw new Error(`Server returned status ${response.status}`);
      }

      const data = await response.json();

      setDashboardData((prev) => ({
        ...prev,
        ...data,
        messages: data.conversation?.messages || prev.messages,
        persona: data.persona || prev.persona,
        investigation: data.investigation || prev.investigation,
        report: data.report || prev.report
      }));
    } catch (err) {
      console.error("Analysis request error:", err);
      setErrorMessage("Undercover trace failed. Verify API connectivity.");
    } finally {
      setIsThinking(false);
      setIsLoading(false);
    }
  };

  // Reset / New investigation
  const handleNewInvestigation = async () => {
    setIsLoading(true);
    try {
      const apiUrl = getApiUrl();
      await fetch(`${apiUrl}/new`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId })
      });
    } catch (err) {
      console.warn("Could not reset backend state:", err);
    }

    setSessionId(generateSessionId());
    setDashboardData(JSON.parse(JSON.stringify(INITIAL_DASHBOARD_DATA)));
    setTimerSeconds(0);
    setIsLoading(false);
    setErrorMessage(null);
  };

  const handleChangePersona = () => {
    alert("Undercover cover identity is configured automatically by the Adaptive Investigation Engine depending on threat context.");
  };

  const handleEndInvestigation = () => {
    if (window.confirm("End trace and generate investigation report archive?")) {
      alert("Investigation completed. Click Generate Report to download.");
    }
  };

  const handleViewPersona = () => {
    if (!dashboardData.persona?.name || dashboardData.persona.name === "Not Assigned") {
      alert("Identity unassigned. Submit a message payload to select a profile.");
      return;
    }
    alert(`Cover identity: ${dashboardData.persona.name}\nProfile: ${dashboardData.persona.occupation}\nRisk Approach: Cautious`);
  };

  const handleShowNotImplemented = (feature) => {
    alert(`${feature} archives are accessible in platform logs.`);
  };

  const handleGenerateReport = () => {
    if (!dashboardData.report) {
      alert("No report generated. Enter scammer dialogue lines to update analysis metrics.");
      return;
    }
    setIsReportOpen(true);
  };

  return (
    <>
      {/* Sidebar */}
      <Sidebar
        onNewInvestigation={handleNewInvestigation}
        onGenerateReport={handleGenerateReport}
        onShowNotImplemented={handleShowNotImplemented}
        isDark={isDark}
        onToggleDark={handleToggleDark}
      />

      {/* Main Container */}
      <div className="main">
        {/* Topbar */}
        <Topbar
          session={dashboardData.session}
          liveTimerText={formatTimer()}
          hasReport={Boolean(dashboardData.report)}
          onChangePersona={handleChangePersona}
          onEndInvestigation={handleEndInvestigation}
          onGenerateReport={handleGenerateReport}
        />

        {/* 3-Panel Content Row */}
        <div className="content-row">
          {/* Left Panel: Persona */}
          <PersonaPanel
            persona={dashboardData.persona}
            confidenceScore={dashboardData.investigation?.confidenceScore || 0}
            isSkeleton={dashboardData.messages?.length === 0}
            onViewPersona={handleViewPersona}
          />

          {/* Center Panel: Live Undercover Chat */}
          <ChatPanel
            messages={dashboardData.messages}
            persona={dashboardData.persona}
            isThinking={isThinking}
            thinkingStep={thinkingStep}
            isLoading={isLoading}
            onSendMessage={handleSendMessage}
            onPasteTemplate={() => {}}
          />

          {/* Right Panel: Investigation Overview */}
          <OverviewPanel
            investigation={dashboardData.investigation}
            onViewAllActivity={() => alert("Viewing full chronological traces.")}
          />
        </div>
      </div>

      {/* Report Modal */}
      <ReportModal
        isOpen={isReportOpen}
        report={dashboardData.report}
        onClose={() => setIsReportOpen(false)}
      />

      {/* Error Toast */}
      <ErrorToast
        message={errorMessage}
        onClose={() => setErrorMessage(null)}
      />
    </>
  );
}
