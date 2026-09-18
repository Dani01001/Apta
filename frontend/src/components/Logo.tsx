export function Logo({ className = "h-9 w-9" }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 40 40"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      aria-hidden="true"
    >
      <rect width="40" height="40" rx="12" className="fill-brand-500" />
      <path
        d="M13 10v9.5c0 1.93 1.57 3.5 3.5 3.5S20 21.43 20 19.5V10"
        stroke="white"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path d="M16.5 10v20" stroke="white" strokeWidth="2" strokeLinecap="round" />
      <path
        d="M25 10c-2.21 0-4 2.24-4 5s1.79 5 4 5v10"
        stroke="white"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
