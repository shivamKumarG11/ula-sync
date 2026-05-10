import { useState } from "react";
import { Send, Bot, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Spinner } from "@/components/ui/Spinner";
import { useAIStore } from "@/store/aiStore";
import { useAIChat } from "@/hooks/useAI";
import { cn } from "@/utils/cn";

export function AIChatbot() {
  const { chatHistory, isChatOpen, isLoading, toggleChat } = useAIStore();
  const { mutate: sendMessage } = useAIChat();
  const [input, setInput] = useState("");

  const handleSend = () => {
    const msg = input.trim();
    if (!msg) return;
    setInput("");
    sendMessage(msg);
  };

  return (
    <>
      <button
        type="button"
        onClick={toggleChat}
        className="fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-primary text-primary-foreground shadow-lg hover:bg-primary/90 transition-colors"
        aria-label="Open AI chat"
      >
        <Bot className="h-6 w-6" />
      </button>

      <AnimatePresence>
        {isChatOpen && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            className="fixed bottom-24 right-6 z-50 w-80 rounded-xl border bg-background shadow-2xl flex flex-col overflow-hidden"
            style={{ maxHeight: "60vh" }}
          >
            <div className="flex items-center justify-between px-4 py-3 border-b bg-primary text-primary-foreground">
              <span className="font-semibold text-sm flex items-center gap-2">
                <Bot className="h-4 w-4" /> Traveloop AI
              </span>
              <button type="button" aria-label="Close chat" onClick={toggleChat}>
                <X className="h-4 w-4" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-3">
              {chatHistory.length === 0 && (
                <p className="text-xs text-muted-foreground text-center">
                  Ask me anything about your trip!
                </p>
              )}
              {chatHistory.map((msg, i) => (
                <div
                  key={i}
                  className={cn(
                    "max-w-[85%] rounded-xl px-3 py-2 text-sm",
                    msg.role === "user"
                      ? "self-end bg-primary text-primary-foreground"
                      : "self-start bg-muted",
                  )}
                >
                  {msg.content}
                </div>
              ))}
              {isLoading && (
                <div className="self-start">
                  <Spinner size="sm" />
                </div>
              )}
            </div>

            <div className="flex gap-2 p-3 border-t">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask me anything…"
                className="flex-1 h-9 text-sm"
                onKeyDown={(e) => e.key === "Enter" && handleSend()}
              />
              <Button size="icon" className="h-9 w-9" onClick={handleSend} disabled={isLoading}>
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
