"use client";

import { useState } from "react";
import { ApiResponse } from "@/types/fraud";

type FileUploadProps = {
  onResult: (data: ApiResponse) => void;
};

export function FileUpload({ onResult }: FileUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;

    try {
      setLoading(true);

      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/predict`,
        {
          method: "POST",
          body: formData,
        },
      );

      if (!response.ok) {
        const errorData = await response.json();

        throw new Error(
          errorData.detail ||
            "Failed to analyze CSV. Please check your file format.",
        );
      }

      const result = await response.json();
      onResult(result);
    } catch (error) {
  console.error(error);

  alert(
    error instanceof Error
      ? error.message
      : "Something went wrong while analyzing the file."
  );
} finally {
  setLoading(false);
}
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 mb-8">
      <label className="block text-sm font-medium mb-3">
        Upload transaction CSV
      </label>

      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="block w-full text-sm text-slate-300 file:mr-4 file:rounded-lg file:border-0 file:bg-cyan-500 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-slate-950 hover:file:bg-cyan-400"
      />

      <button
        onClick={handleUpload}
        disabled={!file || loading}
        className="mt-5 rounded-lg bg-cyan-500 px-5 py-2 font-semibold text-slate-950 disabled:opacity-50"
      >
        {loading ? "Analyzing..." : "Run Fraud Detection"}
      </button>
    </div>
  );
}
