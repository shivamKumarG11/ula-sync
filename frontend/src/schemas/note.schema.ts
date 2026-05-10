import { z } from "zod";

export const noteSchema = z.object({
  title: z.string().max(200).optional(),
  content: z.string().min(1, "Note content is required"),
  stop_id: z.number().int().positive().optional(),
});

export type NoteFormInput = z.infer<typeof noteSchema>;
