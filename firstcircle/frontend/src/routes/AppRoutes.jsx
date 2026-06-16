import { Routes, Route } from "react-router-dom";

import Landing from "../pages/Landing.jsx";
import ProfileSetup from "../pages/ProfileSetup.jsx";
import Dashboard from "../pages/Dashboard.jsx";
import BrowseDrops from "../pages/BrowseDrops.jsx";
import DropDetails from "../pages/DropDetails.jsx";
import CreateDrop from "../pages/CreateDrop.jsx";
import AutoPlace from "../pages/AutoPlace.jsx";
import ProposalPage from "../pages/ProposalPage.jsx";
import ConfirmedCircle from "../pages/ConfirmedCircle.jsx";
import CircleHistory from "../pages/CircleHistory.jsx";
import Feedback from "../pages/Feedback.jsx";
import NotFound from "../pages/NotFound.jsx";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/profile" element={<ProfileSetup />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/drops" element={<BrowseDrops />} />
      <Route path="/drops/:id" element={<DropDetails />} />
      <Route path="/create-drop" element={<CreateDrop />} />
      <Route path="/auto-place" element={<AutoPlace />} />
      <Route path="/proposal" element={<ProposalPage />} />
      <Route path="/confirmed-circle" element={<ConfirmedCircle />} />
      <Route path="/history" element={<CircleHistory />} />
      <Route path="/feedback" element={<Feedback />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}