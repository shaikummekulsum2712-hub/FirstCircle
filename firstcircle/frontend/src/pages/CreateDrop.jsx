import { useNavigate } from "react-router-dom";
import PageWrapper from "../components/layout/PageWrapper.jsx";
import CreateDropForm from "../components/drops/CreateDropForm.jsx";
import useDrops from "../hooks/useDrops.js";

export default function CreateDrop() {
  const navigate = useNavigate();
  const { addDrop } = useDrops();

  function handleCreate(drop) {
    addDrop(drop);
    navigate("/drops");
  }

  return (
    <PageWrapper>
      <div className="mx-auto max-w-4xl">
        <section className="mb-6 rounded-[2rem] bg-gradient-to-br from-orange-100 via-pink-100 to-purple-100 p-8 shadow-soft">
          <p className="font-black text-pink-600">Create a Drop</p>
          <h1 className="mt-1 text-4xl font-black text-slate-950">
            Start a new campus Circle
          </h1>
          <p className="mt-2 text-slate-600">
            Pick the purpose, time, safe place, group size, and vibe. People can
            join the request, but names stay hidden first.
          </p>
        </section>

        <section className="rounded-[2rem] bg-white p-6 shadow-soft">
          <CreateDropForm onCreate={handleCreate} />
        </section>
      </div>
    </PageWrapper>
  );
}