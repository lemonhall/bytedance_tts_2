// 对话TTS编辑器前端逻辑

// 全局状态
const state = {
    currentProjectId: null,
    currentProject: null,
    config: null
};

// DOM元素
const elements = {
    // 步骤面板
    stepInput: document.getElementById('stepInput'),
    stepEdit: document.getElementById('stepEdit'),
    stepPreview: document.getElementById('stepPreview'),
    
    // 输入
    inputText: document.getElementById('inputText'),
    analyzeBtn: document.getElementById('analyzeBtn'),
    
    // 编辑
    projectTitle: document.getElementById('projectTitle'),
    projectMeta: document.getElementById('projectMeta'),
    speakersList: document.getElementById('speakersList'),
    dialoguesList: document.getElementById('dialoguesList'),
    generateAllBtn: document.getElementById('generateAllBtn'),
    backToInputBtn: document.getElementById('backToInputBtn'),
    
    // 预览
    finalAudio: document.getElementById('finalAudio'),
    downloadLink: document.getElementById('downloadLink'),
    backToEditBtn: document.getElementById('backToEditBtn'),
    
    // 工具栏
    newProjectBtn: document.getElementById('newProjectBtn'),
    loadProjectBtn: document.getElementById('loadProjectBtn'),
    
    // 加载提示
    loadingOverlay: document.getElementById('loadingOverlay'),
    loadingText: document.getElementById('loadingText'),
    
    // 模态框
    projectsModal: document.getElementById('projectsModal'),
    projectsListContainer: document.getElementById('projectsListContainer')
};

// 初始化
async function init() {
    try {
        // 加载配置
        const response = await fetch('/api/config');
        state.config = await response.json();
        
        // 绑定事件
        bindEvents();
        
        console.log('✅ 初始化完成');
    } catch (error) {
        console.error('初始化失败:', error);
        showError('初始化失败: ' + error.message);
    }
}

// 绑定事件
function bindEvents() {
    // 分析按钮
    elements.analyzeBtn.addEventListener('click', handleAnalyze);
    
    // 生成全部音频
    elements.generateAllBtn.addEventListener('click', handleGenerateAll);
    
    // 返回按钮
    elements.backToInputBtn.addEventListener('click', () => showStep('input'));
    elements.backToEditBtn.addEventListener('click', () => showStep('edit'));
    
    // 工具栏
    elements.newProjectBtn.addEventListener('click', handleNewProject);
    elements.loadProjectBtn.addEventListener('click', handleLoadProject);
    
    // 模态框关闭
    document.querySelector('.modal-close').addEventListener('click', () => {
        elements.projectsModal.classList.add('hidden');
    });
}

// 显示步骤
function showStep(step) {
    elements.stepInput.classList.remove('active');
    elements.stepEdit.classList.remove('active');
    elements.stepPreview.classList.remove('active');
    
    switch (step) {
        case 'input':
            elements.stepInput.classList.add('active');
            break;
        case 'edit':
            elements.stepEdit.classList.add('active');
            break;
        case 'preview':
            elements.stepPreview.classList.add('active');
            break;
    }
}

// 显示加载
function showLoading(text = '处理中...') {
    elements.loadingText.textContent = text;
    elements.loadingOverlay.classList.remove('hidden');
}

// 隐藏加载
function hideLoading() {
    elements.loadingOverlay.classList.add('hidden');
}

// 错误提示
function showError(message) {
    alert('❌ ' + message);
}

// 成功提示
function showSuccess(message) {
    alert('✅ ' + message);
}

// 处理分析
async function handleAnalyze() {
    const text = elements.inputText.value.trim();
    
    if (!text) {
        showError('请输入对话文本');
        return;
    }
    
    try {
        showLoading('AI正在分析对话...');
        
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        
        if (!response.ok) {
            throw new Error('分析失败');
        }
        
        const data = await response.json();
        state.currentProjectId = data.project_id;
        state.currentProject = data.project;
        
        // 渲染编辑界面
        renderEditPage();
        showStep('edit');
        
    } catch (error) {
        showError('分析失败: ' + error.message);
    } finally {
        hideLoading();
    }
}

// 渲染编辑页面
function renderEditPage() {
    const project = state.currentProject;
    
    // 工程信息
    elements.projectTitle.value = project.title;
    elements.projectMeta.textContent = `共 ${project.speakers.length} 个说话人, ${project.dialogues.length} 句对话`;
    
    // 渲染说话人
    renderSpeakers(project.speakers);
    
    // 渲染对话
    renderDialogues(project.dialogues, project.speakers);
}

// 渲染说话人
function renderSpeakers(speakers) {
    const html = speakers.map(speaker => {
        const icon = speaker.gender === 'male' ? '👨' : 
                     speaker.gender === 'female' ? '👩' : '👶';
        
        return `
            <div class="speaker-card">
                <div class="speaker-card-header">
                    <div class="speaker-icon">${icon}</div>
                    <div class="speaker-info">
                        <input type="text" value="${speaker.name}" 
                               data-speaker-id="${speaker.id}" 
                               class="speaker-name-input">
                    </div>
                </div>
                <div class="speaker-meta">
                    <span class="tag">${getGenderText(speaker.gender)}</span>
                    <span class="tag">${getAgeText(speaker.age_group)}</span>
                </div>
            </div>
        `;
    }).join('');
    
    elements.speakersList.innerHTML = html;
}

// 渲染对话列表
function renderDialogues(dialogues, speakers) {
    const html = dialogues.map((dialogue, index) => {
        const speaker = speakers.find(s => s.id === dialogue.speaker_id);
        const speakerName = speaker ? speaker.name : '未知';
        
        return `
            <div class="dialogue-item" data-line-id="${dialogue.id}">
                <div class="dialogue-header">
                    <span class="dialogue-speaker">${index + 1}. ${speakerName}</span>
                    <div class="dialogue-actions">
                        <button class="btn btn-primary btn-regenerate" data-line-id="${dialogue.id}">
                            🔄 重新生成
                        </button>
                    </div>
                </div>
                
                <textarea class="dialogue-text" data-field="text">${dialogue.text}</textarea>
                
                <div class="dialogue-params">
                    <div class="param-group">
                        <label>情感</label>
                        <select data-field="emotion">
                            <option value="">无</option>
                            ${state.config.emotions.chinese.map(e => 
                                `<option value="${e}" ${dialogue.emotion === e ? 'selected' : ''}>${e}</option>`
                            ).join('')}
                        </select>
                    </div>
                    
                    <div class="param-group">
                        <label>语速 (${dialogue.speed_ratio})</label>
                        <input type="range" min="0.2" max="3.0" step="0.1" 
                               value="${dialogue.speed_ratio}" 
                               data-field="speed_ratio">
                    </div>
                    
                    <div class="param-group">
                        <label>音量 (${dialogue.volume_ratio})</label>
                        <input type="range" min="0.1" max="3.0" step="0.1" 
                               value="${dialogue.volume_ratio}" 
                               data-field="volume_ratio">
                    </div>
                    
                    <div class="param-group">
                        <label>音调 (${dialogue.pitch_ratio})</label>
                        <input type="range" min="0.1" max="3.0" step="0.1" 
                               value="${dialogue.pitch_ratio}" 
                               data-field="pitch_ratio">
                    </div>
                </div>
            </div>
        `;
    }).join('');
    
    elements.dialoguesList.innerHTML = html;
    
    // 绑定对话编辑事件
    bindDialogueEvents();
}

// 绑定对话编辑事件
function bindDialogueEvents() {
    // 文本编辑
    document.querySelectorAll('.dialogue-text').forEach(textarea => {
        textarea.addEventListener('change', handleDialogueUpdate);
    });
    
    // 参数调整
    document.querySelectorAll('.dialogue-params select, .dialogue-params input').forEach(input => {
        input.addEventListener('change', function() {
            // 更新滑块显示的值
            if (this.type === 'range') {
                const label = this.parentElement.querySelector('label');
                const field = this.dataset.field;
                label.textContent = `${getFieldLabel(field)} (${this.value})`;
            }
            handleDialogueUpdate.call(this);
        });
    });
    
    // 重新生成按钮
    document.querySelectorAll('.btn-regenerate').forEach(btn => {
        btn.addEventListener('click', handleRegenerateLine);
    });
}

// 处理对话更新
async function handleDialogueUpdate(event) {
    const dialogueItem = event.target.closest('.dialogue-item');
    const lineId = dialogueItem.dataset.lineId;
    const field = event.target.dataset.field;
    let value = event.target.value;
    
    // 类型转换
    if (event.target.type === 'range') {
        value = parseFloat(value);
    }
    
    try {
        const response = await fetch(`/api/projects/${state.currentProjectId}/line/${lineId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ [field]: value })
        });
        
        if (!response.ok) {
            throw new Error('更新失败');
        }
        
        console.log(`✅ 已更新 ${field}: ${value}`);
        
    } catch (error) {
        showError('更新失败: ' + error.message);
    }
}

// 处理重新生成单句
async function handleRegenerateLine(event) {
    const lineId = event.currentTarget.dataset.lineId;
    
    if (!confirm('确定要重新生成这句对话的音频吗?')) {
        return;
    }
    
    try {
        showLoading('正在生成音频...');
        
        const response = await fetch(`/api/projects/${state.currentProjectId}/generate-line/${lineId}`, {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error('生成失败');
        }
        
        const data = await response.json();
        showSuccess('音频生成成功!');
        
        // 可以在这里添加音频预览功能
        
    } catch (error) {
        showError('生成失败: ' + error.message);
    } finally {
        hideLoading();
    }
}

// 处理生成全部音频
async function handleGenerateAll() {
    if (!confirm(`确定要生成全部 ${state.currentProject.dialogues.length} 句对话的音频吗? 这可能需要一些时间。`)) {
        return;
    }
    
    try {
        showLoading('正在生成音频,请稍候...');
        
        const response = await fetch(`/api/projects/${state.currentProjectId}/generate`, {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error('生成失败');
        }
        
        const data = await response.json();
        
        // 设置音频播放器
        elements.finalAudio.src = data.audio_url;
        elements.downloadLink.href = data.audio_url;
        
        // 显示预览页面
        showStep('preview');
        showSuccess('全部音频生成完成!');
        
    } catch (error) {
        showError('生成失败: ' + error.message);
    } finally {
        hideLoading();
    }
}

// 处理新建工程
function handleNewProject() {
    if (state.currentProjectId && !confirm('当前工程未保存,确定要新建工程吗?')) {
        return;
    }
    
    state.currentProjectId = null;
    state.currentProject = null;
    elements.inputText.value = '';
    showStep('input');
}

// 处理加载工程
async function handleLoadProject() {
    try {
        showLoading('加载工程列表...');
        
        const response = await fetch('/api/projects');
        const data = await response.json();
        
        // 渲染工程列表
        const html = data.projects.map(project => `
            <div class="project-list-item" data-project-id="${project.id}">
                <h4>${project.title}</h4>
                <p>创建时间: ${formatDate(project.created_at)}</p>
                <p>更新时间: ${formatDate(project.updated_at)}</p>
            </div>
        `).join('');
        
        elements.projectsListContainer.innerHTML = html || '<p>暂无工程</p>';
        
        // 绑定点击事件
        document.querySelectorAll('.project-list-item').forEach(item => {
            item.addEventListener('click', async () => {
                const projectId = item.dataset.projectId;
                await loadProject(projectId);
                elements.projectsModal.classList.add('hidden');
            });
        });
        
        // 显示模态框
        elements.projectsModal.classList.remove('hidden');
        
    } catch (error) {
        showError('加载失败: ' + error.message);
    } finally {
        hideLoading();
    }
}

// 加载工程
async function loadProject(projectId) {
    try {
        showLoading('加载工程...');
        
        const response = await fetch(`/api/projects/${projectId}`);
        const project = await response.json();
        
        state.currentProjectId = projectId;
        state.currentProject = project;
        
        renderEditPage();
        showStep('edit');
        
    } catch (error) {
        showError('加载失败: ' + error.message);
    } finally {
        hideLoading();
    }
}

// 工具函数
function getGenderText(gender) {
    const map = { male: '男性', female: '女性', child: '儿童' };
    return map[gender] || gender;
}

function getAgeText(age) {
    const map = { 
        child: '儿童', 
        teenager: '青少年', 
        adult: '成年', 
        elder: '老年' 
    };
    return map[age] || age;
}

function getFieldLabel(field) {
    const map = {
        speed_ratio: '语速',
        volume_ratio: '音量',
        pitch_ratio: '音调'
    };
    return map[field] || field;
}

function formatDate(dateString) {
    if (!dateString) return '未知';
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN');
}

// 启动应用
init();
