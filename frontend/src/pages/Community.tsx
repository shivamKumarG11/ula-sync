import { useState } from "react";
import { Plus } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/Button";
import { Modal } from "@/components/ui/Modal";
import { Skeleton } from "@/components/ui/Skeleton";
import { Pagination } from "@/components/shared/Pagination";
import { EmptyState } from "@/components/shared/EmptyState";
import { SearchBar } from "@/components/shared/SearchBar";
import { CommunityPostCard } from "@/components/community/CommunityPostCard";
import { CommunityPostForm } from "@/components/community/CommunityPostForm";
import { PageWrapper } from "@/components/layout/PageWrapper";
import { useCommunityPosts } from "@/hooks/useCommunity";
import { useAuthStore } from "@/store/authStore";
import { useDebounce } from "@/hooks/useDebounce";
import type { CommunityPost } from "@/types/community";

export default function Community() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const [q, setQ] = useState("");
  const [page, setPage] = useState(1);
  const [showForm, setShowForm] = useState(false);
  const [selected, setSelected] = useState<CommunityPost | null>(null);
  const debouncedQ = useDebounce(q, 300);

  const { data, isLoading } = useCommunityPosts({ q: debouncedQ || undefined, page, per_page: 9 });

  return (
    <PageWrapper
      title="Community"
      description="Stories, tips, and experiences from fellow travelers."
      actions={
        isAuthenticated ? (
          <Button onClick={() => setShowForm(true)}>
            <Plus className="h-4 w-4 mr-1" />
            New Post
          </Button>
        ) : undefined
      }
    >
      <SearchBar
        value={q}
        onChange={(v) => { setQ(v); setPage(1); }}
        placeholder="Search posts…"
        className="max-w-sm"
      />

      {isLoading ? (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <Skeleton key={i} className="h-64" />
          ))}
        </div>
      ) : !data?.items?.length ? (
        <EmptyState
          title="No posts yet"
          description="Be the first to share your travel story!"
        />
      ) : (
        <>
          <motion.div
            className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4"
            initial="hidden"
            animate="visible"
            variants={{
              visible: { transition: { staggerChildren: 0.06 } },
            }}
          >
            {data.items.map((post) => (
              <motion.div
                key={post.id}
                variants={{
                  hidden: { opacity: 0, y: 16 },
                  visible: { opacity: 1, y: 0 },
                }}
              >
                <CommunityPostCard post={post} onClick={() => setSelected(post)} />
              </motion.div>
            ))}
          </motion.div>
          <Pagination page={data.page} pages={data.pages} onPageChange={setPage} />
        </>
      )}

      <Modal open={showForm} onClose={() => setShowForm(false)} title="New Post">
        <CommunityPostForm onSuccess={() => setShowForm(false)} />
      </Modal>

      <Modal
        open={!!selected}
        onClose={() => setSelected(null)}
        title={selected?.title ?? ""}
      >
        {selected && (
          <div className="flex flex-col gap-3">
            {selected.cover_photo_url && (
              <img
                src={selected.cover_photo_url}
                alt={selected.title}
                className="rounded-lg w-full h-48 object-cover"
              />
            )}
            <p className="text-xs text-muted-foreground">
              by @{selected.author_username}
            </p>
            <p className="text-sm leading-relaxed">{selected.content}</p>
          </div>
        )}
      </Modal>
    </PageWrapper>
  );
}
