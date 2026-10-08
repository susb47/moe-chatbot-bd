import Link from "next/link";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-6 font-sans text-slate-800">
      <div className="max-w-3xl text-center space-y-10">
        
        {/* Header / Brand */}
        <div>
          <div className="inline-flex items-center justify-center w-24 h-24 bg-emerald-100 rounded-full mb-6 shadow-inner">
            <span className="text-4xl text-emerald-700 font-extrabold tracking-tighter">EduQ</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-emerald-900 mb-4">
            Ministry of Education AI Assistant
          </h1>
          <p className="text-lg text-emerald-700 font-medium">
            ব্যানবেইস • এনসিটিবি • শিক্ষা বোর্ড
          </p>
        </div>

        {/* Vision Statement */}
        <div className="bg-white p-8 rounded-3xl shadow-sm border border-slate-200 text-left relative overflow-hidden">
          <div className="absolute top-0 left-0 w-2 h-full bg-emerald-600"></div>
          <h2 className="text-2xl font-bold text-emerald-800 mb-4">Our Vision</h2>
          <p className="text-slate-600 leading-relaxed text-lg mb-4">
            To empower every student, parent, and educator in Bangladesh with instant, bilingual access to official educational resources. EduQ bridges the information gap by providing accurate, policy-grounded guidance directly from the Ministry of Education, NCTB, and regional Education Boards.
          </p>
          <p className="text-slate-600 leading-relaxed text-lg">
            বাংলাদেশের প্রতিটি শিক্ষার্থী, অভিভাবক এবং শিক্ষককে শিক্ষা মন্ত্রণালয়ের নির্ভুল তথ্য, শিক্ষাক্রম এবং নীতির সাথে তাৎক্ষণিকভাবে যুক্ত করাই আমাদের লক্ষ্য।
          </p>
        </div>

        {/* Call to Action */}
        <div>
          <Link
            href="/chat"
            className="inline-flex items-center gap-2 bg-emerald-700 hover:bg-emerald-800 text-white font-semibold text-lg px-10 py-4 rounded-full shadow-md transition-all hover:-translate-y-1 hover:shadow-lg"
          >
            Chat with Us 
            <span className="text-xl">→</span>
          </Link>
        </div>

      </div>
    </div>
  );
}