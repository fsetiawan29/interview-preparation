import type { TraceFile } from "@/types/trace";
import twoSum from "./samples/two_sum.json";
import containsDuplicate from "./samples/contains_duplicate.json";
import validParentheses from "./samples/valid_parentheses.json";
import binaryTreeLevelOrder from "./samples/binary_tree_level_order.json";
import courseSchedule from "./samples/course_schedule.json";
import reverseLinkedList from "./samples/reverse_linked_list.json";

export interface SampleTrace {
  id: string;
  label: string;
  snapshotType: string;
  data: TraceFile;
}

export const SAMPLE_TRACES: SampleTrace[] = [
  { id: "two-sum", label: "Two Sum", snapshotType: "array", data: twoSum as TraceFile },
  {
    id: "contains-duplicate",
    label: "Contains Duplicate",
    snapshotType: "array",
    data: containsDuplicate as TraceFile,
  },
  {
    id: "valid-parentheses",
    label: "Valid Parentheses",
    snapshotType: "stack",
    data: validParentheses as TraceFile,
  },
  {
    id: "binary-tree-level-order",
    label: "Binary Tree Level Order Traversal",
    snapshotType: "tree",
    data: binaryTreeLevelOrder as TraceFile,
  },
  {
    id: "course-schedule",
    label: "Course Schedule",
    snapshotType: "graph",
    data: courseSchedule as TraceFile,
  },
  {
    id: "reverse-linked-list",
    label: "Reverse Linked List",
    snapshotType: "linked-list",
    data: reverseLinkedList as TraceFile,
  },
];
