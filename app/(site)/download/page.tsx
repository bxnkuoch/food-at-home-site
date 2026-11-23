import { DownloadButtons } from "@/components/DownloadButtons";
import { getSettings } from "@/sanity/lib/settings";

export const metadata = { title: "Download" };

export default async function DownloadPage() {
  const s = await getSettings();
  return (
    <section className="section">
      <div className="wrap narrow center">
        <span className="pill">Get the app</span>
        <h1>Download {s.appName}</h1>
        <p className="lead">{s.downloadNote ?? "We're in beta on iOS. Join through TestFlight to try the latest build."}</p>
        <DownloadButtons s={s} />
        {s.testflightUrl && (
          <ol className="steps">
            <li>Install Apple's free TestFlight app on your iPhone.</li>
            <li>Tap the TestFlight button above on your phone and accept the invite.</li>
            <li>Install {s.appName} from TestFlight. Updates arrive there too.</li>
          </ol>
        )}
      </div>
    </section>
  );
}
