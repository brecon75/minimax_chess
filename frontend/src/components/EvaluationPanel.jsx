function EvaluationPanel({ evaluation, explanation, isThinking }) {
  const formatScore = (val) => {
    if (val === undefined || val === null) return '0.00';
    const num = val / 100;
    return num > 0 ? `+${num.toFixed(2)}` : num.toFixed(2);
  };

  return (
    <div className="bg-[#2a2a2a] border border-[#444] rounded flex flex-col h-full">
      <div className="p-4 border-b border-[#444] flex justify-between items-center">
        <h2 className="text-gray-200 font-bold">Evaluation</h2>
        {evaluation && (
          <div className="text-gray-200 font-mono text-lg">
            {formatScore(evaluation.total)}
          </div>
        )}
      </div>

      <div className="p-4 flex-1 overflow-y-auto text-sm text-gray-300">
        {isThinking && <p className="text-gray-400">Analyzing position...</p>}

        {!evaluation && !isThinking ? (
          <p className="text-gray-500">Make a move to see analysis.</p>
        ) : (
          !isThinking && (
            <>
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div>
                  <div className="text-gray-500 text-xs uppercase mb-1">Material</div>
                  <div className="font-mono">{formatScore(evaluation?.material)}</div>
                </div>
                <div>
                  <div className="text-gray-500 text-xs uppercase mb-1">Position</div>
                  <div className="font-mono">{formatScore(evaluation?.position)}</div>
                </div>
                <div>
                  <div className="text-gray-500 text-xs uppercase mb-1">Mobility</div>
                  <div className="font-mono">{formatScore(evaluation?.mobility)}</div>
                </div>
                <div>
                  <div className="text-gray-500 text-xs uppercase mb-1">King Safety</div>
                  <div className="font-mono">{formatScore(evaluation?.kingSafety)}</div>
                </div>
              </div>

              <div>
                <h3 className="text-gray-400 font-bold mb-2 uppercase text-xs">Reasoning</h3>
                <div className="space-y-2">
                  {explanation && explanation.length > 0 ? (
                    explanation.map((exp, idx) => (
                      <div key={idx} className="flex gap-2">
                        <span className="text-gray-500">{idx + 1}.</span>
                        <span>{exp}</span>
                      </div>
                    ))
                  ) : (
                    <p className="text-gray-500 italic">No significant changes.</p>
                  )}
                </div>
              </div>
            </>
          )
        )}
      </div>
    </div>
  );
}

export default EvaluationPanel;
