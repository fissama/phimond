"use client";
import { useEffect, useState } from "react";
import type { Catalog, Character, Definition, Lineage, Pet } from "@/lib/types";
import { dependencyTree, type Branch } from "@/lib/planner";
type Section = "species" | "skills" | "items" | "maps";
async function api<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, init);
  const data = await response.json();
  if (!response.ok)
    throw new Error(
      data.error ||
        data.message ||
        "The station could not complete this request.",
    );
  return data;
}
const pretty = (value: unknown): string =>
  typeof value === "object" ? JSON.stringify(value) : String(value ?? "—");
const title = (value: string) =>
  value.replaceAll("_", " ").replace(/\b\w/g, (c) => c.toUpperCase());
const recoveredSpecies = new Set([
  "snail", "flower_fairy", "mushroom", "spider", "wolf", "dark_crab",
  "wealth_turtle", "treasure_chest", "sea_demon", "windmill_spirit",
]);
function CreatureArt({ id, name, element, small = false }: {
  id: string; name: string; element?: string; small?: boolean;
}) {
  return recoveredSpecies.has(id)
    ? <img className={small ? "creature-sprite small" : "creature-sprite"}
        src={`/creatures/${id}.png`} alt={name} />
    : <Sigil element={element} small={small} />;
}
function Sigil({
  element = "earth",
  small = false,
}: {
  element?: string;
  small?: boolean;
}) {
  return (
    <svg
      className={small ? "sigil small" : "sigil"}
      viewBox="0 0 220 190"
      role="img"
      aria-label={`${element} field specimen emblem`}
    >
      <circle
        cx="110"
        cy="98"
        r="70"
        fill="none"
        stroke="currentColor"
        strokeWidth=".7"
      />
      <circle
        cx="110"
        cy="98"
        r="59"
        fill="none"
        stroke="currentColor"
        strokeWidth=".5"
        strokeDasharray="2 6"
      />
      <path
        d="M110 150C55 128 68 69 110 35c42 34 55 93 0 115Z"
        fill="currentColor"
        opacity=".12"
      />
      <path
        d="M110 150V51m0 71-28-29m28 11 26-30m-26 61 35-28m-35-20L93 69"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
      />
      <path d="m105 21 5-8 5 8-5 8Zm0 153 5-8 5 8-5 8Z" fill="currentColor" />
    </svg>
  );
}
function Confidence({ entry }: { entry: Definition }) {
  return (
    <span
      className="confidence"
      title={
        entry.source
          ? `Source: ${entry.source}`
          : "No source supplied by the catalog"
      }
    >
      {entry.confidence || "Unclassified"} · research
    </span>
  );
}
function RecipeBranch({
  node,
  catalog,
  choices,
  onChoose,
}: {
  node: Branch;
  catalog: Catalog;
  choices: Record<string, string>;
  onChoose: (id: string, recipe: string) => void;
}) {
  const options = Object.values(catalog.recipes).filter(
    (r) => r.result === node.speciesId,
  );
  return (
    <li>
      <div className="branch">
        <strong>
          {catalog.species[node.speciesId]?.name || node.speciesId}
        </strong>
        {node.cycle ? (
          <p className="error">Circular dependency — branch stopped.</p>
        ) : node.recipe ? (
          <>
            <label className="sr-only" htmlFor={`recipe-${node.speciesId}`}>
              Recipe for {node.speciesId}
            </label>
            <select
              aria-label={`Recipe for ${node.speciesId}`}
              value={node.recipe.id}
              onChange={(e) => onChoose(node.speciesId, e.target.value)}
            >
              {options.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.name}
                </option>
              ))}
            </select>
            <p>
              Parent Lv. {node.recipe.min_level} · Keeper Lv.{" "}
              {node.recipe.min_player_level} · {node.recipe.gold_cost} gold ·{" "}
              {node.recipe.soul_cost} souls
            </p>
            <p>
              {[
                node.recipe.opposite_gender && "Opposite genders",
                node.recipe.same_star && "Same star",
                node.recipe.cross_race && "Cross race",
                node.recipe.consume_parents && "Parents consumed",
              ]
                .filter(Boolean)
                .join(" · ") || "See recipe research for conditions."}
            </p>
            <Confidence entry={node.recipe} />
          </>
        ) : (
          <p>Acquire in the world · no synthesis recipe recorded</p>
        )}
      </div>
      {node.parents.length > 0 && (
        <ul>
          {node.parents.map((child, i) => (
            <RecipeBranch
              key={i}
              node={child}
              catalog={catalog}
              choices={choices}
              onChoose={onChoose}
            />
          ))}
        </ul>
      )}
    </li>
  );
}
function Ancestry({ node, depth = 0 }: { node: Lineage; depth?: number }) {
  return (
    <li>
      <div className="branch">
        <strong>{node.pet.name}</strong>
        <p>
          {node.pet.species_id} · Lv. {node.pet.level} · Generation{" "}
          {node.pet.generation}
          {node.pet.retired ? " · Retired ancestor" : ""}
        </p>
      </div>
      {depth < 32 && node.parents?.length > 0 && (
        <ul>
          {node.parents.map((p, i) => (
            <Ancestry key={`${p.pet.id}-${i}`} node={p} depth={depth + 1} />
          ))}
        </ul>
      )}
    </li>
  );
}
export default function Journal() {
  const [catalog, setCatalog] = useState<Catalog | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [section, setSection] = useState<Section>("species");
  const [query, setQuery] = useState("");
  const [element, setElement] = useState("all");
  const [active, setActive] = useState<Definition | null>(null);
  const [tab, setTab] = useState<"encyclopedia" | "planner" | "journal">(
    "encyclopedia",
  );
  const [target, setTarget] = useState("");
  const [choices, setChoices] = useState<Record<string, string>>({});
  const [character, setCharacter] = useState<Character | null>(null);
  const [authMode, setAuthMode] = useState<"login" | "register">("login");
  const [authError, setAuthError] = useState("");
  const [busy, setBusy] = useState(false);
  const [lineage, setLineage] = useState<Lineage | null>(null);
  const [lineageError, setLineageError] = useState("");
  async function load() {
    setLoading(true);
    setError("");
    try {
      const data = await api<Catalog>("/api/content");
      setCatalog(data);
      setTarget(Object.values(data.recipes)[0]?.result || "");
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  }
  useEffect(() => {
    void load();
    void api<Character>("/api/character")
      .then(setCharacter)
      .catch(() => {});
  }, []);
  const entries = catalog
    ? Object.values(catalog[section]).filter(
        (e) =>
          (
            e.name +
            " " +
            e.id +
            " " +
            pretty(e.race ?? "") +
            " " +
            pretty(e.element ?? "")
          )
            .toLowerCase()
            .includes(query.toLowerCase()) &&
          (element === "all" || e.element === element),
      )
    : [];
  const elements = catalog
    ? [
        ...new Set(
          Object.values(catalog[section])
            .map((d) => d.element)
            .filter((v): v is string => typeof v === "string"),
        ),
      ]
    : [];
  async function authenticate(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true);
    setAuthError("");
    const form = new FormData(event.currentTarget);
    try {
      await api("/api/auth/" + authMode, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: form.get("username"),
          password: form.get("password"),
        }),
      });
      setCharacter(await api<Character>("/api/character"));
    } catch (e) {
      setAuthError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  async function showLineage(pet: Pet) {
    setLineage(null);
    setLineageError("");
    setBusy(true);
    try {
      setLineage(
        await api<Lineage>("/api/lineage/" + encodeURIComponent(pet.id)),
      );
    } catch (e) {
      setLineageError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <div className="shell">
      <aside className="sidebar">
        <a className="brand" href="/">
          ✳{" "}
          <span>
            PHIMOND<small>THE FIELD JOURNAL</small>
          </span>
        </a>
        <div className="issue">
          EXPLORER’S EDITION <span>VOL. 01</span>
        </div>
        <nav aria-label="Main navigation">
          {(
            [
              ["encyclopedia", "01", "Encyclopedia"],
              ["planner", "02", "Synthesis planner"],
              ["journal", "03", "My journal"],
            ] as const
          ).map(([id, n, label]) => (
            <button
              key={id}
              className={tab === id ? "nav active" : "nav"}
              onClick={() => {
                setTab(id);
                setActive(null);
              }}
            >
              <span>{n}</span>
              {label}
              <b>↗</b>
            </button>
          ))}
        </nav>
        <div className="sidebar-note">
          <Sigil />
          <p>
            Every creature has a story.
            <br />
            Every bond begins with curiosity.
          </p>
          <span>NOTES FROM THE LIVING WORLD</span>
        </div>
        <div className="station">
          <i className={catalog ? "online" : ""} />
          {catalog ? "Field station connected" : "Awaiting field station"}
        </div>
      </aside>
      <main>
        <header className="topbar">
          <span>THE NATURALIST’S COMPANION</span>
          <button className="text-button" onClick={() => setTab("journal")}>
            {character ? character.name : "Keeper sign in"} ↗
          </button>
        </header>
        <section className="hero">
          <div>
            <span className="eyebrow">A WORLD WAITING TO BE KNOWN</span>
            <h1>
              {tab === "encyclopedia" ? (
                <>
                  Small wonders.
                  <br />
                  <em>Extraordinary bonds.</em>
                </>
              ) : tab === "planner" ? (
                <>
                  Trace the roots.
                  <br />
                  <em>Imagine what grows.</em>
                </>
              ) : (
                <>
                  Your companions.
                  <br />
                  <em>Your unfolding story.</em>
                </>
              )}
            </h1>
            <p>
              {tab === "encyclopedia"
                ? "A field guide to the creatures, skills, and quiet corners of Phimond. Observe closely. There is always more to discover."
                : tab === "planner"
                  ? "Follow every branch of a synthesis. Explore the recorded dependencies before taking your companions to the ranch."
                  : "Return to your keeper’s journal to meet your companions and follow the generations that came before them."}
            </p>
          </div>
          <div className="hero-stamp">
            <Sigil />
            <span>OBSERVE · DISCOVER · CONNECT</span>
          </div>
        </section>
        {tab === "encyclopedia" && (
          <>
            <div className="section-heading">
              <div>
                <span className="eyebrow">THE LIVING ARCHIVE</span>
                <h2>Field encyclopedia</h2>
              </div>
              <span className="count">
                {catalog
                  ? String(Object.keys(catalog.species).length).padStart(2, "0")
                  : "—"}{" "}
                species documented
              </span>
            </div>
            <div className="toolbar">
              <div className="category-tabs">
                {(["species", "skills", "items", "maps"] as Section[]).map(
                  (s) => (
                    <button
                      key={s}
                      className={section === s ? "selected" : ""}
                      onClick={() => {
                        setSection(s);
                        setElement("all");
                        setActive(null);
                      }}
                    >
                      {s === "species" ? "Creatures" : title(s)}
                    </button>
                  ),
                )}
              </div>
              <div className="filters">
                <label className="search">
                  <span>⌕</span>
                  <input
                    aria-label="Search encyclopedia"
                    placeholder="Search the field notes…"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                  />
                </label>
                {elements.length > 0 && (
                  <select
                    aria-label="Filter by element"
                    value={element}
                    onChange={(e) => setElement(e.target.value)}
                  >
                    <option value="all">All elements</option>
                    {elements.map((e) => (
                      <option key={e}>{e}</option>
                    ))}
                  </select>
                )}
              </div>
            </div>
            {loading ? (
              <div className="empty">Opening the field archive…</div>
            ) : error ? (
              <div className="empty">
                <h3>The field station is quiet.</h3>
                <p>{error}</p>
                <button onClick={load}>Reconnect</button>
              </div>
            ) : (
              <>
                <div className="result-line">
                  <span>
                    {entries.length}{" "}
                    {section === "species" ? "creatures" : section} in this
                    collection
                  </span>
                  <span>CATALOGUE / {section.toUpperCase()}</span>
                </div>
                <div className="card-grid">
                  {entries.map((entry, i) => (
                    <button
                      className={
                        "specimen " + (active?.id === entry.id ? "chosen" : "")
                      }
                      key={entry.id}
                      onClick={() =>
                        setActive(active?.id === entry.id ? null : entry)
                      }
                    >
                      <div className={"specimen-art tone-" + (i % 4)}>
                        <span className="specimen-no">
                          NO. {String(i + 1).padStart(3, "0")}
                        </span>
                        <span className="specimen-stars">
                          {entry.star
                            ? "✦".repeat(Math.min(Number(entry.star), 7))
                            : "✧"}
                        </span>
                        <CreatureArt id={section === "species" ? entry.id : ""} name={entry.name} element={pretty(entry.element || section)} />
                        <span className="specimen-kind">
                          {pretty(entry.race || entry.kind || section)}
                        </span>
                      </div>
                      <div className="specimen-caption">
                        <span>{pretty(entry.element || section)}</span>
                        <h3>
                          {entry.name}
                          <b>↗</b>
                        </h3>
                        <Confidence entry={entry} />
                      </div>
                    </button>
                  ))}
                </div>
                {entries.length === 0 && (
                  <div className="empty">No field notes match your search.</div>
                )}
                {active && (
                  <section className="detail">
                    <div className="section-heading">
                      <h2>{active.name}</h2>
                      <button onClick={() => setActive(null)}>
                        Close details ×
                      </button>
                    </div>
                    <Confidence entry={active} />
                    <dl>
                      {Object.entries(active)
                        .filter(
                          ([k]) => !["name", "id", "confidence"].includes(k),
                        )
                        .map(([k, v]) => (
                          <div key={k}>
                            <dt>{title(k)}</dt>
                            <dd>{pretty(v)}</dd>
                          </div>
                        ))}
                    </dl>
                  </section>
                )}
              </>
            )}
          </>
        )}
        {tab === "planner" && (
          <section className="planner">
            <div className="section-heading">
              <div>
                <span className="eyebrow">FROM ROOT TO POSSIBILITY</span>
                <h2>Synthesis dependencies</h2>
              </div>
            </div>
            {catalog ? (
              <>
                <label className="field">
                  Choose a creature
                  <select
                    value={target}
                    onChange={(e) => setTarget(e.target.value)}
                  >
                    {Object.values(catalog.species).map((s) => (
                      <option key={s.id} value={s.id}>
                        {s.name}
                      </option>
                    ))}
                  </select>
                </label>
                <p className="muted">
                  Each branch is a required parent. Repeated creatures represent
                  separate parent instances. This is a dependency guide;
                  eligibility and outcomes are decided by the game server.
                </p>
                {target && (
                  <ul className="tree">
                    <RecipeBranch
                      node={dependencyTree(target, catalog.recipes, choices)}
                      catalog={catalog}
                      choices={choices}
                      onChoose={(id, value) =>
                        setChoices({ ...choices, [id]: value })
                      }
                    />
                  </ul>
                )}
              </>
            ) : (
              <div className="empty">
                {loading ? "Loading recorded recipes…" : error}
                <button onClick={load}>Reconnect</button>
              </div>
            )}
          </section>
        )}
        {tab === "journal" && (
          <section>
            {!character ? (
              <div className="auth-panel">
                <div>
                  <span className="eyebrow">A PLACE FOR YOUR DISCOVERIES</span>
                  <h2>
                    {authMode === "login"
                      ? "Welcome back, keeper."
                      : "Begin your field journal."}
                  </h2>
                  <p>
                    Sign in with your game account to view your character,
                    companions, and their family trees.
                  </p>
                  <p className="muted">
                    Unappraised potential remains unknown. Your journal only
                    shows what your keeper has discovered.
                  </p>
                </div>
                <form onSubmit={authenticate}>
                  <label className="field">
                    Keeper name
                    <input
                      required
                      name="username"
                      autoComplete="username"
                      minLength={3}
                      maxLength={24}
                      pattern="[A-Za-z0-9_]{3,24}"
                      title="3–24 letters, digits, or underscores"
                    />
                  </label>
                  <label className="field">
                    Password
                    <input
                      required
                      name="password"
                      type="password"
                      maxLength={72}
                      aria-describedby="password-guidance"
                      autoComplete={
                        authMode === "login"
                          ? "current-password"
                          : "new-password"
                      }
                    />
                  </label>
                  <p id="password-guidance" className="muted">
                    Use a 10–72 byte password. Non-ASCII characters may use
                    multiple bytes.
                  </p>
                  <button className="primary" disabled={busy}>
                    {busy
                      ? "Contacting station…"
                      : authMode === "login"
                        ? "Open my journal →"
                        : "Create account →"}
                  </button>
                  {authError && (
                    <p role="alert" className="error">
                      {authError}
                    </p>
                  )}
                  <button
                    type="button"
                    className="text-button"
                    onClick={() => {
                      setAuthMode(authMode === "login" ? "register" : "login");
                      setAuthError("");
                    }}
                  >
                    {authMode === "login"
                      ? "New keeper? Create an account"
                      : "Already a keeper? Sign in"}
                  </button>
                </form>
              </div>
            ) : (
              <>
                <div className="section-heading">
                  <div>
                    <span className="eyebrow">
                      KEEPER RECORD / REVISION {character.revision}
                    </span>
                    <h2>{character.name}</h2>
                    <p>
                      Level {character.level} · {character.gold} gold ·{" "}
                      {catalog?.maps[character.map_id]?.name ||
                        character.map_id}
                    </p>
                  </div>
                  <button
                    disabled={busy}
                    onClick={async () => {
                      setBusy(true);
                      try {
                        await api("/api/auth/logout", { method: "POST" });
                      } catch {
                      } finally {
                        setCharacter(null);
                        setLineage(null);
                        setBusy(false);
                      }
                    }}
                  >
                    Sign out
                  </button>
                </div>
                <div className="card-grid">
                  {(character.pets || [])
                    .filter((p) => !p.retired)
                    .map((p) => (
                      <article className="pet-card" key={p.id}>
                        <CreatureArt id={p.species_id} name={p.name} small />
                        <span className="eyebrow">
                          GENERATION {p.generation} · {p.gender}
                        </span>
                        <h3>{p.name}</h3>
                        <p>
                          {catalog?.species[p.species_id]?.name || p.species_id}{" "}
                          · Lv. {p.level} · {p.star} stars
                        </p>
                        <p>
                          Vitality {p.hp} / {p.max_hp}
                        </p>
                        <p className="muted">
                          {p.appraised
                            ? "Appraised · potential recorded"
                            : "Unappraised · potential undiscovered"}
                        </p>
                        {p.appraised && p.quality && (
                          <details>
                            <summary>Appraised quality</summary>
                            <dl>
                              {Object.entries(p.quality).map(([k, v]) => (
                                <div key={k}>
                                  <dt>{title(k)}</dt>
                                  <dd>{v}</dd>
                                </div>
                              ))}
                            </dl>
                          </details>
                        )}
                        <button disabled={busy} onClick={() => showLineage(p)}>
                          Trace ancestry ↗
                        </button>
                      </article>
                    ))}
                </div>
                {lineageError && (
                  <p role="alert" className="error">
                    {lineageError}
                  </p>
                )}
                {lineage && (
                  <section className="detail">
                    <h2>The lineage of {lineage.pet.name}</h2>
                    <ul className="tree">
                      <Ancestry node={lineage} />
                    </ul>
                  </section>
                )}
                <section className="detail">
                  <h2>Keeper’s satchel</h2>
                  <dl>
                    {Object.entries(character.inventory || {}).map(
                      ([id, qty]) => (
                        <div key={id}>
                          <dt>{catalog?.items[id]?.name || id}</dt>
                          <dd>{qty}</dd>
                        </div>
                      ),
                    )}
                  </dl>
                </section>
              </>
            )}
          </section>
        )}
        <footer>
          <div>
            <span className="footer-mark">✳</span>
            <div>
              <strong>A journal, still being written.</strong>
              <p>
                Research confidence and source notes come from the shared game
                catalog. Reconstructed rules are interpretations, not verified
                original formulas.
              </p>
            </div>
          </div>
          <span>
            PHIMOND FIELD SOCIETY
            <br />
            FIRST EXPEDITION / VOL. 01
          </span>
        </footer>
      </main>
    </div>
  );
}
