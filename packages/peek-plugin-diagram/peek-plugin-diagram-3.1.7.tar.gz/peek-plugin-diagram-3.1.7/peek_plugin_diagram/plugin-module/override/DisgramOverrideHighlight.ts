import { DiagramOverrideBase } from "./DiagramOverrideBase";
import { addTupleType } from "@synerty/vortexjs";
import { DispColor } from "../lookups";
import { diagramTuplePrefix } from "../_private/PluginNames";

@addTupleType
export class DiagramOverrideHighlight extends DiagramOverrideBase {
    public static readonly tupleName =
        diagramTuplePrefix + "DiagramOverrideHightlight";

    private dispKeys_ = [];
    private highlightColor_: DispColor | null = null;
}
