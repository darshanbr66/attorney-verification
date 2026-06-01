// frontend/src/components/ResultCard.jsx
import { toast } from "react-hot-toast";

const ResultCard = ({ result }) => {

  const copyText = (
    value,
    label
  ) => {

    navigator.clipboard.writeText(
      value
    );

    toast.success(
      `${label} copied`
    );

  };

  const confidenceColor = () => {

    if (result.confidence >= 90)
      return "bg-green-500";

    if (result.confidence >= 70)
      return "bg-yellow-500";

    return "bg-red-500";

  };

  return (
    <div
      className="
        mt-10
        bg-white/[0.03]
        border
        border-white/10
        rounded-3xl
        backdrop-blur-xl
        p-8
      "
    >

      <div
        className="
          flex
          items-center
          justify-between
          flex-wrap
          gap-4
        "
      >

        <h2
          className="
            text-3xl
            font-bold
          "
        >
          Verification Result
        </h2>

        <div
          className={`
            px-5
            py-2
            rounded-full
            text-black
            font-bold
            ${confidenceColor()}
          `}
        >
          {result.confidence}% Confidence
        </div>

      </div>

      {/* Attorney Details */}

      <div className="mt-8">

        <h3
          className="
            text-lg
            font-semibold
            text-cyan-400
          "
        >
          Attorney Details
        </h3>

        <div className="mt-4 space-y-3">

          <p>
            <strong>Name:</strong>{" "}
            {result.name}
          </p>

          <p>
            <strong>Registration:</strong>{" "}
            {result.reg_no}
          </p>

          <p>
            <strong>Organization:</strong>{" "}
            {result.organization}
          </p>

        </div>

      </div>

      {/* Contact */}

      <div className="mt-8">

        <h3
          className="
            text-lg
            font-semibold
            text-cyan-400
          "
        >
          Contact Information
        </h3>

        <div className="mt-4 space-y-4">

          <div
            className="
              flex
              justify-between
              items-center
              flex-wrap
              gap-3
            "
          >

            <span>
              {result.email}
            </span>

            <button
              onClick={() =>
                copyText(
                  result.email,
                  "Email"
                )
              }
              className="
                px-4
                py-2
                rounded-xl
                bg-cyan-400
                text-black
                font-semibold
              "
            >
              Copy
            </button>

          </div>

          <div
            className="
              flex
              justify-between
              items-center
              flex-wrap
              gap-3
            "
          >

            <span>
              {result.phone}
            </span>

            <button
              onClick={() =>
                copyText(
                  result.phone,
                  "Phone"
                )
              }
              className="
                px-4
                py-2
                rounded-xl
                bg-cyan-400
                text-black
                font-semibold
              "
            >
              Copy
            </button>

          </div>

        </div>

      </div>

      {/* Source */}

      <div className="mt-8">

        <a
          href={result.source_url}
          target="_blank"
          rel="noreferrer"
          className="
            inline-flex
            px-5
            py-3
            rounded-2xl
            border
            border-white/10
            bg-white/[0.04]
            hover:bg-white/[0.08]
            transition
          "
        >
          Open Source URL →
        </a>

      </div>

    </div>
  );
};

export default ResultCard;