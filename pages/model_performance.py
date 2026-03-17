import streamlit as st
import json
import os
import plotly.graph_objects as go
from pathlib import Path


def render(render_header):
    """Render Model Performance Metrics page"""
    render_header()
    
    st.divider()
    
    st.markdown("""
        <h2 style="color: #39FF14;">📈 Model Performance Metrics</h2>
        <p style="color: #A0AEC0; font-size: 1em;">
            View the performance metrics of the sentiment analysis model.
        </p>
    """, unsafe_allow_html=True)
    
    try:
        # Try to load model metrics
        metrics_path = './models/model_metrics.json'
        
        if os.path.exists(metrics_path):
            with open(metrics_path, 'r') as f:
                metrics = json.load(f)
            
            st.markdown("### 📊 Model Performance Overview")
            
            # Display key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                accuracy = metrics.get('accuracy', 0)
                st.metric(
                    "🎯 Accuracy",
                    f"{accuracy:.2%}",
                    delta="High Confidence" if accuracy > 0.85 else "Good",
                    delta_color="off"
                )
            
            with col2:
                precision = metrics.get('precision', 0)
                st.metric(
                    "🔍 Precision",
                    f"{precision:.2%}",
                    delta="Reliable Predictions" if precision > 0.85 else "Fair",
                    delta_color="off"
                )
            
            with col3:
                recall = metrics.get('recall', 0)
                st.metric(
                    "🎣 Recall",
                    f"{recall:.2%}",
                    delta="Good Coverage" if recall > 0.85 else "Fair",
                    delta_color="off"
                )
            
            with col4:
                f1 = metrics.get('f1_score', 0)
                st.metric(
                    "⚖️ F1-Score",
                    f"{f1:.2%}",
                    delta="Balanced Performance" if f1 > 0.85 else "Fair",
                    delta_color="off"
                )
            
            st.divider()
            
            # Detailed metrics visualization
            st.markdown("### 🔧 Detailed Performance Metrics")
            
            tab1, tab2, tab3 = st.tabs(["📈 Metrics Visualization", "📋 Detailed Report", "ℹ️ Information"])
            
            with tab1:
                # Create gauge charts for each metric
                col1, col2 = st.columns(2)
                
                with col1:
                    # Accuracy gauge
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=accuracy * 100,
                        title={'text': "Accuracy"},
                        domain={'x': [0, 1], 'y': [0, 1]},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': '#4ADE80'},
                            'steps': [
                                {'range': [0, 50], 'color': 'rgba(248, 113, 113, 0.2)'},
                                {'range': [50, 85], 'color': 'rgba(255, 193, 7, 0.2)'},
                                {'range': [85, 100], 'color': 'rgba(74, 222, 128, 0.2)'}
                            ],
                            'threshold': {
                                'line': {'color': '#39FF14', 'width': 4},
                                'thickness': 0.75,
                                'value': 90
                            }
                        },
                        number={'suffix': "%"}
                    ))
                    
                    fig.update_layout(
                        height=350,
                        paper_bgcolor='#121212',
                        font=dict(color='#E2E8F0', family='Lora, serif'),
                        title_font=dict(color='#39FF14')
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # F1-Score gauge
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=f1 * 100,
                        title={'text': "F1-Score"},
                        domain={'x': [0, 1], 'y': [0, 1]},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': '#00FFFF'},
                            'steps': [
                                {'range': [0, 50], 'color': 'rgba(248, 113, 113, 0.2)'},
                                {'range': [50, 85], 'color': 'rgba(255, 193, 7, 0.2)'},
                                {'range': [85, 100], 'color': 'rgba(74, 222, 128, 0.2)'}
                            ],
                            'threshold': {
                                'line': {'color': '#00FFFF', 'width': 4},
                                'thickness': 0.75,
                                'value': 90
                            }
                        },
                        number={'suffix': "%"}
                    ))
                    
                    fig.update_layout(
                        height=350,
                        paper_bgcolor='#121212',
                        font=dict(color='#E2E8F0', family='Lora, serif'),
                        title_font=dict(color='#00FFFF')
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Precision gauge
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=precision * 100,
                        title={'text': "Precision"},
                        domain={'x': [0, 1], 'y': [0, 1]},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': '#FF6B9D'},
                            'steps': [
                                {'range': [0, 50], 'color': 'rgba(248, 113, 113, 0.2)'},
                                {'range': [50, 85], 'color': 'rgba(255, 193, 7, 0.2)'},
                                {'range': [85, 100], 'color': 'rgba(74, 222, 128, 0.2)'}
                            ],
                            'threshold': {
                                'line': {'color': '#FF6B9D', 'width': 4},
                                'thickness': 0.75,
                                'value': 90
                            }
                        },
                        number={'suffix': "%"}
                    ))
                    
                    fig.update_layout(
                        height=350,
                        paper_bgcolor='#121212',
                        font=dict(color='#E2E8F0', family='Lora, serif'),
                        title_font=dict(color='#FF6B9D')
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Recall gauge
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=recall * 100,
                        title={'text': "Recall"},
                        domain={'x': [0, 1], 'y': [0, 1]},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': '#FFA500'},
                            'steps': [
                                {'range': [0, 50], 'color': 'rgba(248, 113, 113, 0.2)'},
                                {'range': [50, 85], 'color': 'rgba(255, 193, 7, 0.2)'},
                                {'range': [85, 100], 'color': 'rgba(74, 222, 128, 0.2)'}
                            ],
                            'threshold': {
                                'line': {'color': '#FFA500', 'width': 4},
                                'thickness': 0.75,
                                'value': 90
                            }
                        },
                        number={'suffix': "%"}
                    ))
                    
                    fig.update_layout(
                        height=350,
                        paper_bgcolor='#121212',
                        font=dict(color='#E2E8F0', family='Lora, serif'),
                        title_font=dict(color='#FFA500')
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                st.markdown("### 📊 Complete Metrics Report")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                        **Core Metrics:**
                        - **Accuracy**: {accuracy:.4f} ({accuracy:.2%})
                        - **Precision**: {precision:.4f} ({precision:.2%})
                        - **Recall**: {recall:.4f} ({recall:.2%})
                        - **F1-Score**: {f1:.4f} ({f1:.2%})
                    """)
                
                with col2:
                    st.markdown(f"""
                        **Model Information:**
                        - **Model Type**: Transformer-based (DistilBERT)
                        - **Classes**: Positive, Negative, Neutral
                        - **Last Updated**: {metrics.get('saved_at', 'N/A')}
                        - **Architecture**: {metrics.get('model_name', 'distilbert-base-uncased-finetuned-sst-2-english')}
                    """)
                
                st.divider()
                
                # Classification report if available
                if 'classification_report' in metrics:
                    st.markdown("### Classification Report by Class")
                    
                    report = metrics['classification_report']
                    
                    report_data = []
                    for class_name in ['negative', 'neutral', 'positive']:
                        if str(class_name) in report or class_name in report:
                            class_metrics = report.get(class_name, report.get(str(class_name), {}))
                            report_data.append({
                                'Class': class_name.upper(),
                                'Precision': f"{class_metrics.get('precision', 0):.4f}",
                                'Recall': f"{class_metrics.get('recall', 0):.4f}",
                                'F1-Score': f"{class_metrics.get('f1-score', 0):.4f}",
                                'Support': int(class_metrics.get('support', 0))
                            })
                    
                    if report_data:
                        import pandas as pd
                        df_report = pd.DataFrame(report_data)
                        st.dataframe(df_report, use_container_width=True, hide_index=True)
            
            with tab3:
                st.markdown("""
                    ### 📚 Model Information
                    
                    **Model Architecture:**
                    - Pre-trained Language Model: DistilBERT
                    - Task: Sentiment Classification
                    - Classes: 3 (Positive, Negative, Neutral)
                    - Fine-tuned on: Reviews and News Data
                    
                    **Performance Interpretation:**
                    
                    - **Accuracy**: Overall correctness of the model's predictions
                    - **Precision**: Among positive predictions, how many are actually correct
                    - **Recall**: Among actual positive cases, how many did the model find
                    - **F1-Score**: Harmonic mean of precision and recall, balanced metric
                    
                    **Benchmark:**
                    - Excellent: F1-Score > 0.90
                    - Very Good: F1-Score > 0.85
                    - Good: F1-Score > 0.80
                    - Fair: F1-Score > 0.70
                    - Needs Improvement: F1-Score < 0.70
                    
                    **Current Model Status:**
                """)
                
                # Determine status
                if f1 > 0.90:
                    status = "🟢 Excellent - Model is performing exceptionally well"
                    color = "#4ADE80"
                elif f1 > 0.85:
                    status = "🟢 Very Good - Model is performing very well"
                    color = "#4ADE80"
                elif f1 > 0.80:
                    status = "🟡 Good - Model is performing well"
                    color = "#FFA500"
                elif f1 > 0.70:
                    status = "🟡 Fair - Model is performing adequately"
                    color = "#FFA500"
                else:
                    status = "🔴 Needs Improvement - Consider retraining"
                    color = "#F87171"
                
                st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, rgba(57, 255, 20, 0.1), rgba(0, 255, 255, 0.1));
                        border-left: 4px solid {color};
                        border-radius: 6px;
                        padding: 15px;
                    ">
                        <p style="color: {color}; margin: 0; font-weight: 600; font-size: 1.1em;">
                            {status}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
        
        else:
            st.info("📊 Model metrics not found. Please train the model first by running `python train_model.py`.")
            
            st.markdown("""
                ### How to Train the Model
                
                1. Open a terminal in the project directory
                2. Run: `python train_model.py`
                3. Wait for training to complete
                4. Metrics will be saved and displayed here
            """)
    
    except Exception as e:
        st.error(f"❌ Error loading metrics: {str(e)}")
    
    st.divider()
    
    # Back button
    col1, col2 = st.columns([8, 2])
    
    with col2:
        if st.button("↩️ Back to Home", use_container_width=True, key="back_from_performance"):
            st.session_state.selected_page = None
            st.rerun()
