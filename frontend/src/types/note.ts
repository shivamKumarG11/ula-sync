export interface TripNote {
  id: number;
  trip_id: number;
  stop_id: number | null;
  title: string | null;
  content: string;
  created_at: string;
  updated_at: string;
}

export interface NoteCreateInput {
  content: string;
  title?: string;
  stop_id?: number;
}

export interface NoteUpdateInput {
  content?: string;
  title?: string;
}
