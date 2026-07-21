import { useRef } from "react";
import { FileJson } from "lucide-react";
import { Button } from "@/components/ui/button";

export function FilePicker({ onFile }: { onFile: (file: File) => void }) {
  const inputRef = useRef<HTMLInputElement>(null);

  return (
    <>
      <Button type="button" variant="outline" onClick={() => inputRef.current?.click()}>
        <FileJson />
        Choose a file
      </Button>
      <input
        ref={inputRef}
        type="file"
        accept="application/json,.json"
        className="hidden"
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) onFile(file);
          e.target.value = "";
        }}
      />
    </>
  );
}
