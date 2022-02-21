package thedrake;

import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;

public class TroopTile  implements Tile, JSONSerializable {
    private final Troop troop;
    private final PlayingSide side;
    private final TroopFace face;

    public TroopTile(Troop troop, PlayingSide side, TroopFace face) {
        this.troop = troop;
        this.side = side;
        this.face = face;
    }

    public PlayingSide side() {
        return side;
    }

    public TroopFace face(){
        return face;
    }
    public Troop troop(){
        return troop;
    }
    public boolean canStepOn(){
        return false;
    }
    public boolean hasTroop() {
        return true;
    }
    public TroopTile flipped(){
        TroopFace new_face;
        if(face==TroopFace.AVERS)
            new_face= TroopFace.REVERS;
        else
            new_face=TroopFace.AVERS;
        TroopTile new_tile= new  TroopTile(this.troop, this.side, new_face);
        return  new_tile;
    }

    @Override
    public List<Move> movesFrom(BoardPos pos, GameState state) {
        List<Move> result = new ArrayList<Move>();
        if(pos == BoardPos.OFF_BOARD)
            return result;
        List<TroopAction> actions = troop().actions(face);
        for (TroopAction act : actions) {
            for(Move mv : act.movesFrom(pos, side, state)){
                result.add(mv);
            }
        }
        return result;
    }

    @Override
    public String toString() {
        return "\"troop\":" + "\"" +troop.name() + "\"," + "\"side\":" + "\"" + side.name() + "\"," + "\"face\":" + "\"" + face.name() + "\"";
    }

    @Override
    public void toJSON(PrintWriter writer) {
        writer.print("{");
        writer.print("\"troop\":\"" + troop.name());
        writer.print("\",\"side\":");
        side.toJSON(writer);
        writer.print(",\"face\":");
        face.toJSON(writer);
        writer.print("}");
    }


}
