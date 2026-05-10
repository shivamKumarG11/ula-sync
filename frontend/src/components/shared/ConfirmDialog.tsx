import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalTitle,
} from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";

interface ConfirmDialogProps {
  open: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title?: string;
  description?: string;
  confirmLabel?: string;
  isPending?: boolean;
}

export function ConfirmDialog({
  open,
  onClose,
  onConfirm,
  title = "Are you sure?",
  description = "This action cannot be undone.",
  confirmLabel = "Delete",
  isPending,
}: ConfirmDialogProps) {
  return (
    <Modal open={open} onOpenChange={(v) => !v && onClose()}>
      <ModalContent>
        <ModalHeader>
          <ModalTitle>{title}</ModalTitle>
        </ModalHeader>
        <p className="text-sm text-muted-foreground">{description}</p>
        <div className="flex justify-end gap-2 mt-4">
          <Button variant="outline" onClick={onClose} disabled={isPending}>
            Cancel
          </Button>
          <Button
            variant="destructive"
            onClick={onConfirm}
            disabled={isPending}
          >
            {isPending ? "Deleting…" : confirmLabel}
          </Button>
        </div>
      </ModalContent>
    </Modal>
  );
}
