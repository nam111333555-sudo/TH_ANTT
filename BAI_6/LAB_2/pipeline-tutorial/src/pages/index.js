import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

const steps = [
  ['01', 'Build', 'Cài đặt đúng phiên bản thư viện và tạo website tĩnh bằng Docusaurus.'],
  ['02', 'Test', 'Kiểm tra cấu hình đường dẫn, phát hiện lỗi build và liên kết bị hỏng.'],
  ['03', 'Deploy', 'Chuyển artifact sang GitLab Pages sau khi các bước trước thành công.'],
];

export default function Home() {
  return (
    <Layout title="Bảo mật với DevSecOps" description="Bài thực hành GitLab CI/CD và Docusaurus">
      <main>
        <section className="lab-hero">
          <div className="container">
            <p className="lab-eyebrow">THỰC HÀNH / LẬP TRÌNH AN NINH THÔNG TIN</p>
            <h1>Bảo mật bắt đầu<br />từ mỗi lần commit.</h1>
            <p className="lab-lead">Bài 6: xây dựng pipeline CI/CD với GitLab, tự động build Docusaurus và triển khai lên GitLab Pages.</p>
            <div className="lab-actions">
              <Link className="button button--primary button--lg" to="/docs/intro">Bắt đầu thực hành →</Link>
              <Link className="button button--secondary button--lg" to="/docs/submission">Checklist nộp bài</Link>
            </div>
            <div className="lab-flow" aria-label="Quy trình CI/CD">COMMIT <span>→</span> BUILD <span>→</span> TEST <span>→</span> PAGES</div>
          </div>
        </section>
        <section className="container lab-section">
          <p className="lab-eyebrow">TỪ MÃ NGUỒN ĐẾN TRIỂN KHAI</p>
          <h2>Một quy trình có thể kiểm chứng.</h2>
          <div className="lab-grid">
            {steps.map(([number, title, text]) => (
              <article className="lab-card" key={number}>
                <span className="lab-number">{number}</span><h3>{title}</h3><p>{text}</p>
              </article>
            ))}
          </div>
          <p className="lab-note">Đây là tài liệu thực hành. Trạng thái pipeline và kết quả triển khai thực tế được xem trực tiếp trong dự án GitLab.</p>
        </section>
      </main>
    </Layout>
  );
}
