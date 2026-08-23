import { LoaderCircle } from "lucide-react";
export default function LoadingState({ message = "Processing..." }) {
  return <div className="loading-state"><LoaderCircle className="spin" size={27}/><span>{message}</span></div>;
}