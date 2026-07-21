import { registerViewer } from "@/utils/viewerRegistry";
import { ArrayViewer } from "./ArrayViewer";
import { StackViewer } from "./StackViewer";
import { QueueViewer } from "./QueueViewer";
import { TreeViewer } from "./TreeViewer";
import { GraphViewer } from "./GraphViewer";
import { LinkedListViewer } from "./LinkedListViewer";

registerViewer("array", ArrayViewer);
registerViewer("stack", StackViewer);
registerViewer("queue", QueueViewer);
registerViewer("tree", TreeViewer);
registerViewer("graph", GraphViewer);
registerViewer("linked-list", LinkedListViewer);
