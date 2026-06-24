import { Chessboard } from 'react-chessboard';

function ChessBoardUI({ game, onDrop, disabled = false }) {
  return (
    <Chessboard 
      position={game.fen()} 
      onPieceDrop={onDrop}
      arePiecesDraggable={!disabled}
      autoPromoteToQueen
      customDarkSquareStyle={{ backgroundColor: '#444' }}
      customLightSquareStyle={{ backgroundColor: '#888' }}
      animationDuration={300}
      customBoardStyle={{
        borderRadius: '0px',
        boxShadow: 'none',
      }}
    />
  );
}

export default ChessBoardUI;
