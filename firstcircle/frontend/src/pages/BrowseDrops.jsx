import { useState } from "react";
import { useNavigate } from "react-router-dom";
import PageWrapper from "../components/layout/PageWrapper.jsx";
import DropCard from "../components/drops/DropCard.jsx";
import DropFilters from "../components/drops/DropFilters.jsx";
import Modal from "../components/common/Modal.jsx";
import Button from "../components/common/Button.jsx";
import useDrops from "../hooks/useDrops.js";

export default function BrowseDrops() {
  const navigate = useNavigate();
  const { drops, joinDrop } = useDrops();
  const [filter, setFilter] = useState("all");
  const [selectedDrop, setSelectedDrop] = useState(null);

  const visibleDrops = filter === "all" ? drops : drops.filter((drop) => drop.type === filter);

  function handleJoin(drop) {
    joinDrop(drop.id);
    setSelectedDrop(drop);
  }

  return (
    <PageWrapper>
      <div className="mb-8 flex flex-col justify-between gap-4 md:flex-row md:items-end">
        <div>
          <p className="font-black text-orange-600">Circle Drops</p>
          <h1 className="text-4xl font-black text-slate-950">Browse open Drops</h1>
          <p className="mt-2 text-slate-600">Choose a purpose, not a person. Names stay hidden first.</p>
        </div>
        <DropFilters activeFilter={filter} onChange={setFilter} />
      </div>

      <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
        {visibleDrops.map((drop) => (
          <DropCard key={drop.id} drop={drop} onJoin={handleJoin} />
        ))}
      </div>

      <Modal
        open={Boolean(selectedDrop)}
        title="You joined the request 👻"
        onClose={() => setSelectedDrop(null)}
      >
        {selectedDrop && (
          <div>
            <p className="text-slate-600">
              You joined <b>{selectedDrop.title}</b>. When enough people are interested,
              FirstCircle will send a blind proposal.
            </p>

            <div className="mt-5 rounded-3xl bg-yellow-50 p-4">
              <p className="font-black text-slate-900">What happens next?</p>
              <ul className="mt-2 space-y-2 text-sm text-slate-600">
                <li>✅ We wait for enough interested people.</li>
                <li>👻 Names stay hidden.</li>
                <li>🎉 If enough accept, the Circle is confirmed.</li>
              </ul>
            </div>

            <div className="mt-5 grid grid-cols-2 gap-3">
              <Button variant="secondary" onClick={() => setSelectedDrop(null)}>Keep Browsing</Button>
              <Button variant="purple" onClick={() => navigate("/proposal")}>See Demo Proposal</Button>
            </div>
          </div>
        )}
      </Modal>
    </PageWrapper>
  );
}