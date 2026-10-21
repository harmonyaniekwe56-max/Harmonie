import json
from pathlib import Path
from datetime import datetime

import streamlit as st

st.set_page_config(page_title="Harmony AI", page_icon="✍️", layout="wide")

LIBRARY_FILE = Path("harmony_library.json")

def load_library():
    if LIBRARY_FILE.exists():
        try:
            return json.loads(LIBRARY_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []

def save_library(items):
    LIBRARY_FILE.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")

st.title("✍️ Harmony AI")
st.caption("A creative space for writers to develop story ideas, organize drafts, and keep a writing journal.")

page = st.sidebar.radio(
    "Menu",
    ["Home", "Story Writer", "My Library", "Writing Journal", "Help"],
)

if page == "Home":
    st.subheader("Welcome to Harmony AI")
    st.write("Your writing space for building characters, exploring plots, and keeping your ideas together.")
    st.info("This starter version uses writing prompts and templates. It does not yet connect to an AI model.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ✨ Develop an idea")
        st.write("Turn a small idea into a story outline.")
    with col2:
        st.markdown("### 📚 Keep your work")
        st.write("Save drafts to the app's local storage.")

elif page == "Story Writer":
    st.subheader("Story Writer")
    title = st.text_input("Story title", placeholder="e.g. The Secret Beyond the Gate")
    genre = st.selectbox("Genre", ["Fantasy", "Romance", "Mystery", "Adventure", "Science fiction", "Realistic fiction", "Other"])
    idea = st.text_area("Your story idea", placeholder="Tell Harmony AI what happens in your story...", height=150)
    goal = st.selectbox("What would you like help with?", ["Build a plot outline", "Create a character", "Plan the opening scene", "Find possible conflicts"])
    if st.button("Develop my idea", type="primary"):
        if not idea.strip():
            st.warning("Write a short story idea first.")
        else:
            if goal == "Build a plot outline":
                result = f"""# {title or 'Untitled Story'} — {genre}\n\n**Beginning:** Introduce the main character, their ordinary life, and what they want.\n\n**Inciting incident:** Something unexpected interrupts that life: {idea.strip()}\n\n**Rising action:** Add two or three obstacles that make the character's goal harder to reach.\n\n**Turning point:** Reveal a discovery or decision that changes the character's plan.\n\n**Climax:** Bring the character face-to-face with the biggest challenge.\n\n**Ending:** Show what has changed and what the character has learned."""
            elif goal == "Create a character":
                result = f"""# Character concept\n\n**Role:** Main character in a {genre.lower()} story\n\n**Starting point:** {idea.strip()}\n\n**Goal:** What the character wants most\n\n**Strength:** A skill or quality that helps them\n\n**Flaw:** A habit or fear that complicates things\n\n**Secret:** Something they are not ready to share\n\n**Character arc:** How their choices may change them"""
            elif goal == "Plan the opening scene":
                result = f"""# Opening scene plan\n\n**Setting:** Choose a vivid place that fits your {genre.lower()} story.\n\n**First image:** Show the character doing something specific.\n\n**Immediate problem:** {idea.strip()}\n\n**Dialogue or action:** Let the character react in their own voice.\n\n**Scene hook:** End with a question, surprise, or decision that makes the reader want to continue."""
            else:
                result = f"""# Possible conflicts\n\nStarting idea: {idea.strip()}\n\n1. **External conflict:** Someone or something blocks the character's goal.\n2. **Relationship conflict:** Two characters want different things.\n3. **Inner conflict:** The character must face a fear or difficult choice.\n4. **Mystery:** A detail does not make sense yet.\n5. **Stakes:** Decide what the character might lose if they fail."""
            st.markdown(result)
            st.download_button("Download this draft", result, file_name="harmony_draft.md", mime="text/markdown")
            if st.button("Save draft to My Library"):
                items = load_library()
                items.append({"title": title or "Untitled Story", "genre": genre, "goal": goal, "idea": idea, "draft": result, "saved_at": datetime.now().isoformat(timespec="minutes")})
                save_library(items)
                st.success("Draft saved to the library.")

elif page == "My Library":
    st.subheader("My Library")
    items = load_library()
    if not items:
        st.write("Your library is empty. Create a draft in Story Writer and save it here.")
    else:
        for i, item in enumerate(reversed(items)):
            with st.expander(f"{item.get('title', 'Untitled Story')} — {item.get('genre', 'Other')}"):
                st.caption(f"Saved: {item.get('saved_at', 'Unknown')}")
                st.write(item.get("idea", ""))
                st.markdown(item.get("draft", ""))
                st.download_button("Download draft", item.get("draft", ""), file_name=f"harmony_draft_{i+1}.md", key=f"download_{i}")

elif page == "Writing Journal":
    st.subheader("Writing Journal")
    journal = st.text_area("Today's writing notes", placeholder="Record ideas, questions, or what you want to write next...", height=220)
    if st.button("Download journal entry"):
        if journal.strip():
            content = f"# Harmony AI Writing Journal\n\n{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n{journal.strip()}\n"
            st.download_button("Download .txt file", content, file_name="harmony_journal.txt", mime="text/plain")
        else:
            st.warning("Write a few notes first.")

else:
    st.subheader("Help")
    st.markdown("""
- **Story Writer:** Enter an idea and choose a planning tool.
- **My Library:** View drafts saved during this app's current storage lifetime.
- **Writing Journal:** Write notes and download them.
- **Downloads:** Use the download buttons to keep copies on your device.

**Current limitations:** This starter app uses templates, not a connected AI model. Image generation and automatic voice transcription are not enabled yet. Files stored on free hosting may not persist forever, so download important drafts to your device.
""")
