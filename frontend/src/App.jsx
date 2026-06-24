import { useState, useEffect } from 'react';
import axios from 'axios';
import { Chess } from 'chess.js';
import ChessBoardUI from './components/ChessBoardUI';
import EvaluationPanel from './components/EvaluationPanel';
import DifficultySelector from './components/DifficultySelector';
const API_URL = 'http://127.0.0.1:5000';

function App() {
  const [game, setGame] = useState(new Chess());
  const [evaluation, setEvaluation] = useState(null);
  const [explanation, setExplanation] = useState([]);
  const [difficulty, setDifficulty] = useState('Easy');
  const [isEngineThinking, setIsEngineThinking] = useState(false);
  const [gameOverMsg, setGameOverMsg] = useState(null);
  
  // Initialize game
  useEffect(() => {
    startNewGame();
  }, []);

  const startNewGame = async () => {
    try {
      const res = await axios.post(`${API_URL}/new-game`);
      setGame(new Chess(res.data.fen));
      setEvaluation(null);
      setExplanation([]);
      setGameOverMsg(null);
    } catch (err) {
      console.error('Failed to start game', err);
    }
  };

  const onDrop = async (sourceSquare, targetSquare) => {
    if (isEngineThinking || game.isGameOver()) return false;
    
    // Check if move is legal
    const move = {
      from: sourceSquare,
      to: targetSquare,
      promotion: 'q',
    };
    
    try {
      // Validate locally first
      const gameCopy = new Chess(game.fen());
      const legalMove = gameCopy.move(move);
      if (!legalMove) return false;
      const playerMoveUci = `${legalMove.from}${legalMove.to}${legalMove.promotion ?? ''}`;
      
      // Update local state for immediate feedback
      setGame(gameCopy);
      setIsEngineThinking(true);
      
      if (gameCopy.isGameOver()) {
        checkGameOver(gameCopy);
        setIsEngineThinking(false);
        return true;
      }
      
      // Send move to backend
      const res = await axios.post(`${API_URL}/move`, {
        fen: game.fen(),
        move: playerMoveUci,
        difficulty: difficulty
      });
      
      // Update from backend response
      const newGame = new Chess(res.data.fen);
      setGame(newGame);
      setEvaluation(res.data.evaluation);
      setExplanation(res.data.explanation);
      
      if (res.data.game_over) {
        checkGameOver(newGame);
      }
      
      setIsEngineThinking(false);
      return true;
    } catch (err) {
      console.error('Error making move', err);
      // Revert if backend error
      setGame(new Chess(game.fen()));
      setIsEngineThinking(false);
      return false;
    }
  };

  const checkGameOver = (chessInstance) => {
    if (chessInstance.isCheckmate()) {
      setGameOverMsg(`Checkmate! ${chessInstance.turn() === 'w' ? 'Black' : 'White'} wins.`);
    } else if (chessInstance.isDraw()) {
      setGameOverMsg('Game Over: Draw');
    } else if (chessInstance.isStalemate()) {
      setGameOverMsg('Game Over: Stalemate');
    }
  };

  return (
    <div className="min-h-screen p-6 md:p-12 flex flex-col max-w-5xl mx-auto">
      
      <header className="mb-6 flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-200">Chess Engine</h1>
          <p className="text-gray-400 text-sm mt-1">Play against AI and see its evaluation.</p>
        </div>
        <div className="flex gap-4">
          <DifficultySelector difficulty={difficulty} setDifficulty={setDifficulty} disabled={isEngineThinking} />
          <button 
            onClick={startNewGame}
            disabled={isEngineThinking}
            className="px-4 py-2 bg-[#2a2a2a] hover:bg-[#333] border border-[#444] rounded text-sm text-gray-200 transition-colors disabled:opacity-50"
          >
            New Game
          </button>
        </div>
      </header>

      <div className="flex flex-col md:flex-row gap-8">
        
        {/* Left Column - Board */}
        <div className="w-full md:w-[600px] shrink-0 relative">
          {isEngineThinking && (
            <div className="absolute inset-0 bg-[#1a1a1a]/50 z-10 flex items-center justify-center">
              <div className="bg-[#2a2a2a] px-4 py-2 border border-[#444] rounded text-gray-200 text-sm">
                Thinking...
              </div>
            </div>
          )}
          <div className="w-full aspect-square border border-[#444]">
            <ChessBoardUI game={game} onDrop={onDrop} disabled={isEngineThinking || game.isGameOver()} />
          </div>
        </div>

        {/* Right Column - Explainability Panel */}
        <div className="flex-1 flex flex-col gap-4">
          {gameOverMsg && (
            <div className="bg-[#2a2a2a] border border-[#444] p-4 rounded text-gray-200">
              <p className="font-bold">{gameOverMsg}</p>
            </div>
          )}
          <EvaluationPanel evaluation={evaluation} explanation={explanation} isThinking={isEngineThinking} />
        </div>
        
      </div>
      
    </div>
  );
}

export default App;
