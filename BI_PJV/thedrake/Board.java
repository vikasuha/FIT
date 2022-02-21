package thedrake;

import java.io.PrintWriter;

public class Board implements JSONSerializable{
	private final int dimension;
	private BoardTile [][]  GameBoard;
	// Konstruktor. Vytvoří čtvercovou hrací desku zadaného rozměru, kde všechny dlaždice jsou prázdné, tedy BoardTile.EMPTY
	public Board(int dimension) {
		this.dimension=dimension;
		this.GameBoard=new BoardTile[dimension][dimension];
		for (int i=0; i<dimension;i++)
		{
			for( int j=0; j<dimension;j++)
			{
				GameBoard[i][j]= BoardTile.EMPTY;
			}
		}

	}

	// Rozměr hrací desky
	public int dimension() {
		return dimension;
		// Místo pro váš kód
	}

	// Vrací dlaždici na zvolené pozici.
	public BoardTile at(BoardPos pos) {
		return GameBoard[pos.i()][pos.j()];
	}

	// Vytváří novou hrací desku s novými dlaždicemi. Všechny ostatní dlaždice zůstávají stejné
	public Board withTiles(TileAt ...ats) {
		Board new_board= new Board(this.dimension);
		for (int i=0; i<dimension;i++)
		{
			for( int j=0; j<dimension;j++)
			{
				new_board.GameBoard[i][j]= this.GameBoard[i][j];
			}
		}
		for(TileAt i: ats) {
			new_board.GameBoard[i.pos.i()][i.pos.j()] = i.tile;
		}
		return new_board;
	}

	// Vytvoří instanci PositionFactory pro výrobu pozic na tomto hracím plánu
	public PositionFactory positionFactory() {
		PositionFactory new_factory= new PositionFactory(this.dimension);
		return new_factory;
	}
	
	public static class TileAt {
		public final BoardPos pos;
		public final BoardTile tile;
		
		public TileAt(BoardPos pos, BoardTile tile) {
			this.pos = pos;
			this.tile = tile;
		}
	}

	@Override
	public void toJSON(PrintWriter writer) {
		writer.print("{");
		writer.print("\"dimension\":" + dimension);
		writer.print(",\"tiles\":[");

		for (int i = 0; i < GameBoard.length; i++) {
			for (int j = 0; j < GameBoard[i].length; j++) {
				GameBoard[j][i].toJSON(writer);
				if (!(i == GameBoard.length - 1 && j == GameBoard[i].length - 1)) writer.print(",");
			}
		}

		writer.print("]}");
	}


}

