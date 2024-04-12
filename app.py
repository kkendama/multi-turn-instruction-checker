import streamlit as st
import json

jsonl_file = 'wiki-multi-turn-v4.jsonl'

# JSONLファイルを読み込む
with open(jsonl_file, 'r', encoding='utf-8') as f:
    conversations = [json.loads(line) for line in f]

def save_conversations():
    with open(jsonl_file, 'w', encoding='utf-8') as f:
        for conversation in conversations:
            f.write(json.dumps(conversation, ensure_ascii=False) + '\n')

def display_conversation(conversation):
    st.markdown(f"### {conversation['text_title']}")
    st.write(f"Text: {conversation['text']}")
    st.markdown("### Chat")

    chat_parts = conversation['chat'].split('ASSISTANT:')
    chat_parts = [chat_part.split('USER:') for chat_part in chat_parts]
    chat_parts = [item for sublist in chat_parts for item in sublist][1:]

    chat_markdown = ""
    for i, part in enumerate(chat_parts):
        if i % 2 == 0:  # USER
            chat_markdown += f"**USER:** {part.strip()}\n\n"
        else:  # ASSISTANT
            chat_markdown += f"**ASSISTANT:** {part.strip()}\n\n"

    st.markdown(chat_markdown)

def main():
    st.title('Conversation Quality Evaluation')

    if 'current_idx' not in st.session_state:
        st.session_state.current_idx = next((i for i, c in enumerate(conversations) if 'isOK' not in c), 0)

    conversation = conversations[st.session_state.current_idx]
    display_conversation(conversation)

    is_ok = st.radio(f"Is this conversation OK?", ('Not evaluated', 'OK', 'NG'), index=0)
    if is_ok == 'OK':
        conversation['isOK'] = True
    elif is_ok == 'NG':
        conversation['isOK'] = False

    edited_chat = st.text_area("Edit conversation if needed:", value=conversation['chat'], key=f"edit_{st.session_state.current_idx}", height=300)
    
    if st.button("Save edited conversation"):
        conversation['chat'] = edited_chat
        save_conversations()
        st.experimental_rerun()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Previous conversation") and st.session_state.current_idx > 0:
            st.session_state.current_idx -= 1
            st.experimental_rerun()

    with col2:
        if st.button("Next conversation"):
            save_conversations()
            next_idx = next((i for i, c in enumerate(conversations[st.session_state.current_idx + 1:], start=st.session_state.current_idx + 1) if 'isOK' not in c), None)
            if next_idx is not None:
                st.session_state.current_idx = next_idx
            else:
                st.warning("No more conversations to evaluate.")
            st.experimental_rerun()

if __name__ == '__main__':
    main()