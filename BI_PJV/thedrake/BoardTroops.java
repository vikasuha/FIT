package thedrake;

import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Optional;
import java.util.Set;


public class BoardTroops implements JSONSerializable{
	private final PlayingSide playingSide;
	private final Map<BoardPos, TroopTile> troopMap;
	private final TilePos leaderPosition;
	private final int guards;
	
	public BoardTroops(PlayingSide playingSide) {
		this(playingSide,
				Collections.emptyMap(),
				TilePos.OFF_BOARD,
				0);

	}
	
	public BoardTroops(
			PlayingSide playingSide,
			Map<BoardPos, TroopTile> troopMap,
			TilePos leaderPosition, 
			int guards) {
		this.playingSide=playingSide;
		this.troopMap=troopMap;
		this.leaderPosition=leaderPosition;
		this.guards=guards;

	}

	public Optional<TroopTile> at(TilePos pos) {

		return Optional.ofNullable(troopMap.get(pos));
	}
	
	public PlayingSide playingSide() {

		return playingSide;
	}
	
	public TilePos leaderPosition() {
			return leaderPosition;
	}

	public int guards() {

		return guards;
	}
	
	public boolean isLeaderPlaced() {
		return leaderPosition() != TilePos.OFF_BOARD;
	}
	
	public boolean isPlacingGuards() {
		return leaderPosition != TilePos.OFF_BOARD && guards < 2;
	}	
	
	public Set<BoardPos> troopPositions() {
		return troopMap.keySet();
	}

	public BoardTroops placeTroop(Troop troop, BoardPos target) {
		if(at(target).isPresent())
			throw new IllegalArgumentException();

		Map<BoardPos, TroopTile> newTroops = new HashMap<>(troopMap);
		newTroops.put(target, new TroopTile(troop, playingSide, TroopFace.AVERS));

		int newGuards = guards;
		if(isPlacingGuards())
			newGuards++;

		TilePos newLeaderPos = leaderPosition;
		if(leaderPosition == TilePos.OFF_BOARD) {
			newLeaderPos = target;
		}

		return new BoardTroops(playingSide(), newTroops, newLeaderPos, newGuards);


	}
	
	public BoardTroops troopStep(BoardPos origin, BoardPos target) {
		if(!isLeaderPlaced()) {
			throw new IllegalStateException(
					"Cannot move troops before the leader is placed.");
		}

		if(isPlacingGuards()) {
			throw new IllegalStateException(
					"Cannot move troops before guards are placed.");
		}

		if(!at(origin).isPresent())
			throw new IllegalArgumentException();

		if(at(target).isPresent())
			throw new IllegalArgumentException();

		Map<BoardPos, TroopTile> newTroops = new HashMap<>(troopMap);
		TroopTile tile = newTroops.remove(origin);
		newTroops.put(target, tile.flipped());

		TilePos newLeaderPos = leaderPosition;
		if(leaderPosition.equals(origin)) {
			newLeaderPos = target;
		}

		return new BoardTroops(playingSide(), newTroops, newLeaderPos, guards);


	}

	
	public BoardTroops troopFlip(BoardPos origin) {
		if(!isLeaderPlaced()) {
			throw new IllegalStateException(
					"Cannot move troops before the leader is placed.");
		}

		if(isPlacingGuards()) {
			throw new IllegalStateException(
					"Cannot move troops before guards are placed.");
		}

		if(!at(origin).isPresent())
			throw new IllegalArgumentException();

		Map<BoardPos, TroopTile> newTroops = new HashMap<>(troopMap);
		TroopTile tile = newTroops.remove(origin);
		newTroops.put(origin, tile.flipped());

		return new BoardTroops(playingSide(), newTroops, leaderPosition, guards);
	}

	public BoardTroops removeTroop(BoardPos target) {
		if(!isLeaderPlaced()) {
			throw new IllegalStateException(
					"Cannot move troops before the leader is placed.");
		}

		if(isPlacingGuards()) {
			throw new IllegalStateException(
					"Cannot move troops before guards are placed.");
		}

		if(!at(target).isPresent())
			throw new IllegalArgumentException();

		Map<BoardPos, TroopTile> newTroops = new HashMap<>(troopMap);
		newTroops.remove(target);

		TilePos newLeaderPos = leaderPosition;
		if(leaderPosition.equals(target)) {
			newLeaderPos = TilePos.OFF_BOARD;
		}

		return new BoardTroops(playingSide(), newTroops, newLeaderPos, guards);

	}

	@Override
	public void toJSON(PrintWriter writer) {
		writer.print("{");
		writer.print("\"side\":");
		playingSide.toJSON(writer);
		writer.print(",\"leaderPosition\":");
		leaderPosition.toJSON(writer);
		writer.print(",\"guards\":" + guards);
		writer.print(",\"troopMap\":");

		writer.print("{");
		ArrayList<Map.Entry<BoardPos, TroopTile>> troops = new ArrayList<>(troopMap.entrySet());
		troops.sort(Comparator.comparing(a -> a.getKey().toString()));
		Iterator<Map.Entry<BoardPos, TroopTile>> iter = troops.iterator();
		while (iter.hasNext()) {
			Map.Entry<BoardPos, TroopTile> cur = iter.next();
			cur.getKey().toJSON(writer);
			writer.print(":");
			cur.getValue().toJSON(writer);
			if (iter.hasNext()) writer.print(",");

		}
		writer.print("}");
		writer.print("}");
	}


}
