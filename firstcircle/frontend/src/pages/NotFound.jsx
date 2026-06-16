import { Link } from "react-router-dom";
import PageWrapper from "../components/layout/PageWrapper.jsx";
import Button from "../components/common/Button.jsx";

export default function NotFound() {
  return (
    <PageWrapper>
      <div className="grid min-h-[60vh] place-items-center text-center">
        <div>
          <div className="text-7xl">🫠</div>
          <h1 className="mt-4 text-4xl font-black text-slate-900">Page not found</h1>
          <p className="mt-2 text-slate-600">This Circle does not exist yet.</p>
          <Link to="/dashboard">
            <Button className="mt-6">Go Home</Button>
          </Link>
        </div>
      </div>
    </PageWrapper>
  );
}