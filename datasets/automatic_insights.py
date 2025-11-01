import pandas as pd
from datetime import datetime

class SimpleInsightsDetector:
    def __init__(self, metrics_path: str, orders_path: str):
        self.df_metrics = pd.read_csv(metrics_path)
        self.df_orders = pd.read_csv(orders_path)
        self.week_cols = ['L8W_ROLL', 'L7W_ROLL', 'L6W_ROLL', 'L5W_ROLL', 
                         'L4W_ROLL', 'L3W_ROLL', 'L2W_ROLL', 'L1W_ROLL', 'L0W_ROLL']
    
    def detect_anomalies(self):
        "Detect >10% week-over-week changes"
        results = []
        for _, row in self.df_metrics.iterrows():
            current = row['L0W_ROLL']
            previous = row['L1W_ROLL']
            
            if pd.notna(current) and pd.notna(previous) and previous != 0:
                change = ((current - previous) / abs(previous)) * 100
                
                if abs(change) > 10:
                    results.append({
                        'zone': f"{row['ZONE']} - {row['CITY']} ({row['COUNTRY']})",
                        'metric': row['METRIC'],
                        'change_pct': round(change, 2),
                        'type': 'Mejora' if change > 0 else 'Deterioro'
                    })
        
        return sorted(results, key=lambda x: abs(x['change_pct']), reverse=True)[:20]
    
    def detect_worrying_trends(self):
        "Detect 3+ consecutive weeks of decline"
        results = []
        for _, row in self.df_metrics.iterrows():
            values = [row[col] for col in self.week_cols[-4:]]  # Last 4 weeks
            
            if all(pd.notna(v) for v in values):
                if values[1] < values[0] and values[2] < values[1] and values[3] < values[2]:
                    total_decline = ((values[3] - values[0]) / abs(values[0])) * 100
                    
                    results.append({
                        'zone': f"{row['ZONE']} - {row['CITY']} ({row['COUNTRY']})",
                        'metric': row['METRIC'],
                        'decline_pct': round(total_decline, 2),
                        'weeks': 3
                    })
        
        return sorted(results, key=lambda x: abs(x['decline_pct']), reverse=True)[:15]
    
    def detect_benchmarking(self):
        "Compare similar zones (same country/type)"
        results = []
        grouped = self.df_metrics.groupby(['COUNTRY', 'ZONE_TYPE', 'METRIC'])
        
        for (country, zone_type, metric), group in grouped:
            if len(group) < 3:
                continue
            
            values = group['L0W_ROLL'].dropna()
            if len(values) < 3:
                continue
            
            mean_val = values.mean()
            std_val = values.std()
            
            if std_val == 0:
                continue
            
            for _, row in group.iterrows():
                val = row['L0W_ROLL']
                if pd.notna(val):
                    z_score = (val - mean_val) / std_val
                    
                    if abs(z_score) > 1.5:
                        results.append({
                            'zone': f"{row['ZONE']} - {row['CITY']} ({row['COUNTRY']})",
                            'metric': metric,
                            'zone_type': zone_type,
                            'value': round(val, 2),
                            'peer_avg': round(mean_val, 2),
                            'deviation_pct': round(((val - mean_val) / mean_val) * 100, 2),
                            'status': 'Mejor' if z_score > 0 else 'Peor'
                        })
        
        return sorted(results, key=lambda x: abs(x['deviation_pct']), reverse=True)[:20]
    
    def detect_correlations(self):
        "Find metric correlations"
        pivot = self.df_metrics.pivot_table(
            index=['COUNTRY', 'CITY', 'ZONE'],
            columns='METRIC',
            values='L0W_ROLL'
        ).reset_index()
        
        results = []
        metric_pairs = [
            ('Lead Penetration', 'Perfect Orders'),
            ('Gross Profit UE', 'Perfect Orders'),
            ('Pro Adoption (Last Week Status)', '% PRO Users Who Breakeven')
        ]
        
        for m1, m2 in metric_pairs:
            if m1 in pivot.columns and m2 in pivot.columns:
                valid = pivot[[m1, m2, 'ZONE', 'CITY', 'COUNTRY']].dropna()
                
                if len(valid) > 10:
                    corr = valid[m1].corr(valid[m2])
                    median1 = valid[m1].median()
                    median2 = valid[m2].median()
                    
                    problematic = valid[(valid[m1] < median1) & (valid[m2] < median2)]
                    
                    if abs(corr) > 0.3 and len(problematic) > 0:
                        results.append({
                            'metric1': m1,
                            'metric2': m2,
                            'correlation': round(corr, 3),
                            'problematic_zones_count': len(problematic),
                            'sample_zones': [
                                f"{z['ZONE']} - {z['CITY']} ({z['COUNTRY']})" 
                                for _, z in problematic.head(5).iterrows()
                            ]
                        })
        
        return results
    
    def generate_and_save(self, output_path: str):
        "Generate all insights and save to file"
        print("Generando insights...")
        
        anomalies = self.detect_anomalies()
        trends = self.detect_worrying_trends()
        benchmarks = self.detect_benchmarking()
        correlations = self.detect_correlations()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("REPORTE DE INSIGHTS AUTOMÁTICOS - RAPPI\n")
            f.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            # 1. Anomalías
            f.write("1. ANOMALÍAS (Cambios >10% semana a semana)\n")
            f.write("-"*80 + "\n")
            for i, a in enumerate(anomalies, 1):
                f.write(f"{i}. {a['zone']}\n")
                f.write(f"   Métrica: {a['metric']}\n")
                f.write(f"   Cambio: {a['change_pct']}% ({a['type']})\n\n")
            
            # 2. Tendencias
            f.write("\n2. TENDENCIAS PREOCUPANTES (3+ semanas en declive)\n")
            f.write("-"*80 + "\n")
            for i, t in enumerate(trends, 1):
                f.write(f"{i}. {t['zone']}\n")
                f.write(f"   Métrica: {t['metric']}\n")
                f.write(f"   Declive total: {t['decline_pct']}% en {t['weeks']} semanas\n\n")
            
            # 3. Benchmarking
            f.write("\n3. BENCHMARKING (Comparación con zonas similares)\n")
            f.write("-"*80 + "\n")
            for i, b in enumerate(benchmarks, 1):
                f.write(f"{i}. {b['zone']} ({b['zone_type']})\n")
                f.write(f"   Métrica: {b['metric']}\n")
                f.write(f"   Valor: {b['value']} vs Promedio pares: {b['peer_avg']}\n")
                f.write(f"   Desviación: {b['deviation_pct']}% ({b['status']} que pares)\n\n")
            
            # 4. Correlaciones
            f.write("\n4. CORRELACIONES ENTRE MÉTRICAS\n")
            f.write("-"*80 + "\n")
            for i, c in enumerate(correlations, 1):
                f.write(f"{i}. {c['metric1']} <-> {c['metric2']}\n")
                f.write(f"   Correlación: {c['correlation']}\n")
                f.write(f"   Zonas problemáticas (ambas bajas): {c['problematic_zones_count']}\n")
                f.write(f"   Ejemplos: {', '.join(c['sample_zones'][:3])}\n\n")
            
            f.write("\n" + "="*80 + "\n")
            f.write(f"Total: {len(anomalies)} anomalías, {len(trends)} tendencias, ")
            f.write(f"{len(benchmarks)} benchmarks, {len(correlations)} correlaciones\n")
        
        print(f"Insights guardados en: {output_path}")
        return {
            'anomalies': len(anomalies),
            'trends': len(trends),
            'benchmarks': len(benchmarks),
            'correlations': len(correlations)
        }