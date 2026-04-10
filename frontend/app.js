const API_BASE = "/api";

const state = {
    groqKey: localStorage.getItem('groq_key') || "",
    currentIdea: null,
    activePage: 'home',
    mode: 'ideas'
};

document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
    const keyInput = document.getElementById('groq-key-input');
    if (state.groqKey) keyInput.value = state.groqKey;
    keyInput.addEventListener('change', (e) => {
        state.groqKey = e.target.value;
        localStorage.setItem('groq_key', state.groqKey);
    });

    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', () => changePage(btn.dataset.page));
    });

    document.getElementById('search-docs-btn').addEventListener('click', searchKnowledgeBase);
    document.getElementById('send-chat-btn').addEventListener('click', sendChatMessage);
});

function changePage(pageId) {
    state.activePage = pageId;
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.toggle('active', btn.dataset.page === pageId));
    document.querySelectorAll('.page-content').forEach(page => page.classList.toggle('hidden', page.id !== `page-${pageId}`));
    document.getElementById('active-page-title').innerText = pageId.charAt(0).toUpperCase() + pageId.slice(1);
    lucide.createIcons();
}

function setMode(mode) {
    state.mode = mode;
    document.getElementById('form-container').classList.remove('hidden');
    document.querySelectorAll('.mode-form').forEach(f => f.classList.add('hidden'));
    document.getElementById(`form-${mode === 'execution' ? 'execution' : mode}`).classList.remove('hidden');
    document.getElementById('form-container').scrollIntoView({ behavior: 'smooth' });
}

async function handleAction(mode) {
    if (!state.groqKey) return alert("Please enter a Groq API Key.");
    const resultsContainer = document.getElementById('results-container');
    resultsContainer.innerHTML = "<div class='loading'>Processing mission...</div>";

    let data;
    if (mode === 'ideas') {
        data = await apiRequest('/generate', { domain: "high-growth sectors (Tech, Food, Green, AI)", skills: "generalist" });
    } else if (mode === 'validate') {
        const ideaText = document.getElementById('valid-idea').value;
        if (!ideaText) return alert("Please enter a concept to validate.");
        const idea = { name: "Your Custom Venture", description: ideaText };
        renderHorizontalIdeas([idea]);
        selectIdea(idea); // Auto-select for immediate feedback
        return;
    } else {
        data = await apiRequest('/generate', { 
            domain: document.getElementById('exec-domain').value, 
            skills: document.getElementById('exec-skills').value 
        });
    }

    if (data && data.ideas) renderHorizontalIdeas(data.ideas);
}

function renderHorizontalIdeas(ideas) {
    const container = document.getElementById('results-container');
    container.innerHTML = "";
    ideas.forEach(idea => {
        const div = document.createElement('div');
        div.className = "horizontal-idea-card glass-card";
        div.innerHTML = `<h3>${idea.name}</h3><p>${idea.description}</p><div class="card-footer">${idea.target_audience || 'MARKET READY'}</div>`;
        div.onclick = () => selectIdea(idea);
        container.appendChild(div);
    });
}

async function selectIdea(idea) {
    state.currentIdea = idea;
    const detailView = document.getElementById('home-detail-view');
    detailView.classList.remove('hidden');
    
    // Jump to the details
    setTimeout(() => detailView.scrollIntoView({ behavior: 'smooth' }), 100);

    const valBox = document.getElementById('home-val-content');
    valBox.innerHTML = "<div class='loading'>Analyzing competitive landscape...</div>";

    // Parallel fetch for main modules
    const [val, road] = await Promise.all([
        apiRequest('/validate', { idea }),
        apiRequest('/roadmap', { idea, timeline: "6 months" })
    ]);

    console.log("Validation API Response:", val);
    console.log("Roadmap API Response:", road);

    if (val && val.validation_report) {
        valBox.innerHTML = formatMarkdown(val.validation_report);
    } else {
        valBox.innerHTML = "<p style='color:#ff4444;'>Validation failed or returned empty. Check your API key or console.</p>";
    }

    if (road && road.roadmap) {
        document.getElementById('home-road-content').innerHTML = formatMarkdown(road.roadmap);
        document.getElementById('page-roadmap-container').innerHTML = formatMarkdown(road.roadmap);
    } else {
        document.getElementById('home-road-content').innerHTML = "Roadmap generation failed.";
    }
    
    // Auto-fill dashboard & strategy
    simulateGrowth();
    fetchInsights();
}

async function simulateGrowth() {
    const data = await apiRequest('/simulate-growth', { idea: state.currentIdea });
    if (data && data.growth) {
        const chart = document.getElementById('growth-chart');
        chart.innerHTML = "";
        data.growth.forEach(val => {
            const bar = document.createElement('div');
            bar.className = "chart-bar";
            const heightPerc = (val / Math.max(...data.growth)) * 100;
            setTimeout(() => bar.style.height = `${heightPerc}%`, 100);
            chart.appendChild(bar);
        });
    }
}

async function fetchInsights() {
    const data = await apiRequest('/insights', { idea: state.currentIdea });
    if (data && data.insights) {
        const list = document.getElementById('insights-list');
        list.innerHTML = data.insights.map(i => `<div class='insight-item'>${i}</div>`).join('');
    }
}

async function calculateStrategy() {
    if (!state.currentIdea) return alert("Please select an idea first!");
    const budget = document.getElementById('strat-budget').value;
    const age = document.getElementById('strat-age').value;
    const output = document.getElementById('strategy-output');
    
    output.classList.remove('hidden');
    output.innerHTML = "<div class='loading'>Calculating strategic risk/reward...</div>";
    
    const data = await apiRequest('/strategy', { idea: state.currentIdea, budget, age });
    if (data && data.strategy_report) {
        output.innerHTML = `<div class='glass-card' style='padding:30px;'>${formatMarkdown(data.strategy_report)}</div>`;
    }
}

async function searchKnowledgeBase() {
    const query = document.getElementById('research-query').value;
    const box = document.getElementById('research-answer');
    if (!query) return;
    
    box.innerHTML = "<div class='loading'>Consulting industry reports...</div>";
    const data = await apiRequest('/search-docs', { query, idea: state.currentIdea });
    
    if (data && data.answer) {
        box.innerHTML = `<div class='qa-answer'>${formatMarkdown(data.answer)}</div>`;
    } else {
        box.innerHTML = "No specific findings. Try a different query.";
    }
}

async function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const msg = input.value;
    if (!msg) return;
    
    addMessage("user", msg);
    input.value = "";
    
    const data = await apiRequest('/chat', { message: msg, context: state.currentIdea || { status: "Exploring" } });
    if (data && data.response) addMessage("assistant", data.response);
}

function addMessage(role, text) {
    const messages = document.getElementById('chat-messages');
    messages.innerHTML += `<div class="message ${role}">${text}</div>`;
    messages.scrollTop = messages.scrollHeight;
}

async function apiRequest(endpoint, body) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-Groq-Key': state.groqKey },
            body: JSON.stringify(body)
        });
        return await response.json();
    } catch (e) { return null; }
}

function formatMarkdown(text) {
    return text.replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
}

function switchHomeTab(tab) {
    document.querySelectorAll('.home-tab-btn').forEach(btn => btn.classList.toggle('active', btn.onclick.toString().includes(tab)));
    document.getElementById('home-val-content').classList.toggle('hidden', tab !== 'validation');
    document.getElementById('home-road-content').classList.toggle('hidden', tab !== 'roadmap');
}
