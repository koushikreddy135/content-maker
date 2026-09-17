import React, { useState, useEffect } from 'react';
import confetti from 'canvas-confetti';
import Header from './components/Header';
import TopicForm from './components/TopicForm';
import PipelineVisualizer from './components/PipelineVisualizer';
import VersionDiffViewer from './components/VersionDiffViewer';
import FinalPackageView from './components/FinalPackageView';
import ExplainabilityDrawer from './components/ExplainabilityDrawer';
import HistoryModal from './components/HistoryModal';

const API_BASE = 'http://127.0.0.1:8000/api';

export default function App() {
  const [currentJobId, setCurrentJobId] = useState(null);
  const [currentNode, setCurrentNode] = useState('idle');
  const [history, setHistory] = useState(null);
  const [isRunning, setIsRunning] = useState(false);
  const [jobs, setJobs] = useState([]);
  const [isExplainOpen, setIsExplainOpen] = useState(false);
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);

  // Fetch past jobs list on mount
  const fetchJobs = async () => {
    try {
      const res = await fetch(`${API_BASE}/jobs`);
      if (res.ok) {
        const data = await res.json();
        setJobs(data);
        if (data.length > 0 && !currentJobId) {
          loadJob(data[0].id);
        }
      }
    } catch (e) {
      console.error('Failed to fetch jobs:', e);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  const loadJob = async (jobId) => {
    try {
      const res = await fetch(`${API_BASE}/jobs/${jobId}/history`);
      if (res.ok) {
        const data = await res.json();
        setHistory(data);
        setCurrentJobId(jobId);
        setCurrentNode(data.job.current_node);
      }
    } catch (e) {
      console.error('Failed to load job:', e);
    }
  };

  const handleStartGeneration = async (formData) => {
    setIsRunning(true);
    setCurrentNode('research');
    setHistory(null);

    try {
      const res = await fetch(`${API_BASE}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (!res.ok) throw new Error('Submission failed');
      const data = await res.json();
      const jobId = data.job_id;
      setCurrentJobId(jobId);

      // Start SSE stream
      const eventSource = new EventSource(`${API_BASE}/jobs/${jobId}/stream`);

      eventSource.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          if (payload.event === 'node_start') {
            setCurrentNode(payload.data.node);
          } else if (payload.event === 'job_complete' || payload.event === 'pipeline_complete') {
            setIsRunning(false);
            setCurrentNode('completed');
            eventSource.close();
            loadJob(jobId);
            fetchJobs();

            if (payload.status === 'approved' || payload.data?.status === 'approved') {
              confetti({
                particleCount: 80,
                spread: 70,
                origin: { y: 0.6 }
              });
            }
          }
        } catch (err) {
          console.error('SSE parse error:', err);
        }
      };

      eventSource.onerror = () => {
        eventSource.close();
        // Polling fallback
        pollJobCompletion(jobId);
      };

    } catch (err) {
      console.error('Pipeline start error:', err);
      setIsRunning(false);
    }
  };

  const pollJobCompletion = async (jobId) => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${API_BASE}/jobs/${jobId}`);
        if (res.ok) {
          const data = await res.json();
          setCurrentNode(data.current_node);
          if (data.status === 'approved' || data.status === 'escalated_to_human' || data.status === 'failed') {
            clearInterval(interval);
            setIsRunning(false);
            loadJob(jobId);
            fetchJobs();
          }
        }
      } catch (e) {
        clearInterval(interval);
        setIsRunning(false);
      }
    }, 1500);
  };

  return (
    <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '24px 20px' }}>
      <Header
        onOpenHistory={() => setIsHistoryOpen(true)}
        onOpenExplainability={() => setIsExplainOpen(true)}
        currentJob={history?.job}
      />

      <TopicForm onSubmit={handleStartGeneration} isRunning={isRunning} />

      <PipelineVisualizer
        currentNode={currentNode}
        history={history}
        isRunning={isRunning}
      />

      <VersionDiffViewer history={history} />

      <FinalPackageView history={history} />

      <ExplainabilityDrawer
        isOpen={isExplainOpen}
        onClose={() => setIsExplainOpen(false)}
        history={history}
      />

      <HistoryModal
        isOpen={isHistoryOpen}
        onClose={() => setIsHistoryOpen(false)}
        jobs={jobs}
        onSelectJob={loadJob}
      />
    </div>
  );
}
