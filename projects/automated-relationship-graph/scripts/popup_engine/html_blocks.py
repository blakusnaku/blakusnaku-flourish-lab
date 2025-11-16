def title_block(text, color):
    return f"""
    <div style="
        font-size:20px;
        font-weight:700;
        color:{color};
        margin-bottom:12px;
        padding-bottom:6px;
        border-bottom:1px solid rgba(255,255,255,0.15);
    ">
        {text}
    </div>
    """

def small(text, color):
    return f'<div style="font-size:11px; color:{color}; margin-top:2px;">{text}</div>'

def section(title, content, accent):
    return f"""
    <div style="margin-top:8px; font-size:11px;">
      <span style="color:{accent}; font-weight:600;">{title}</span><br>
      {content}
    </div>
    """
