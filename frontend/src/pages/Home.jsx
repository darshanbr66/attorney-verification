// frontend/src/pages/Home.jsx
import { useState } from "react";
import API from "../services/api";

import AttorneyForm from "../components/AttorneyForm";
import ResultCard from "../components/ResultCard";

import toast from "react-hot-toast";

const Home = () => {

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const verifyAttorney = async (data) => {

    try {

      setLoading(true);

      const response =
        await API.post(
          "/verify-attorney",
          data
        );

      setResult(response.data);

      toast.success(
        "Verification Complete"
      );

    } catch (error) {

      toast.error(
        "Verification Failed"
      );

      console.error(error);

    } finally {

      setLoading(false);

    }
  };

  return (

    <div className="
      min-h-screen
      bg-[#020617]
      text-white
    ">

      {/* Sticky Header */}

      <header
        className="
          sticky
          top-0
          z-50

          border-b
          border-white/10

          bg-[#020617]/90
          backdrop-blur-xl
        "
      >

        <div
          className="
            max-w-6xl
            mx-auto
            px-6

            h-20

            flex
            items-center
            justify-between
          "
        >

          <div>

            <h1
              className="
                text-2xl
                font-bold
                tracking-wide
              "
            >
              Sigvitas
            </h1>

            <p
              className="
                text-xs
                text-slate-400
              "
            >
              Attorney Verification Platform
            </p>

          </div>

          <div
            className="
              hidden
              md:flex
              items-center
              gap-3
            "
          >

            <div
              className="
                w-2
                h-2
                rounded-full
                bg-green-400
              "
            />

            <span
              className="
                text-sm
                text-slate-400
              "
            >
              System Online
            </span>

          </div>

        </div>

      </header>

      {/* Main Content */}

      <div
        className="
          max-w-6xl
          mx-auto
          px-6
          py-16
        "
      >

        {/* Hero */}

        <div
          className="
            text-center
            max-w-3xl
            mx-auto
          "
        >

          <h1
            className="
              text-5xl
              md:text-6xl
              font-bold
              leading-tight
            "
          >
            Verify Attorney
            Information Instantly
          </h1>

          <p
            className="
              mt-6
              text-lg
              text-slate-400
              leading-relaxed
            "
          >
            Search attorney records using
            attorney name,
            registration number,
            organization,
            and city.
          </p>

        </div>

        {/* Stats */}

        <div
          className="
            mt-12
            grid
            md:grid-cols-3
            gap-6
          "
        >

          <div
            className="
              rounded-2xl
              border
              border-white/10
              bg-white/[0.03]
              p-6
              text-center
            "
          >

            <h3
              className="
                text-3xl
                font-bold
                text-cyan-400
              "
            >
              5000+
            </h3>

            <p
              className="
                mt-2
                text-slate-400
              "
            >
              Attorneys Verified
            </p>

          </div>

          <div
            className="
              rounded-2xl
              border
              border-white/10
              bg-white/[0.03]
              p-6
              text-center
            "
          >

            <h3
              className="
                text-3xl
                font-bold
                text-cyan-400
              "
            >
              95%
            </h3>

            <p
              className="
                mt-2
                text-slate-400
              "
            >
              Verification Accuracy
            </p>

          </div>

          <div
            className="
              rounded-2xl
              border
              border-white/10
              bg-white/[0.03]
              p-6
              text-center
            "
          >

            <h3
              className="
                text-3xl
                font-bold
                text-cyan-400
              "
            >
              Instant
            </h3>

            <p
              className="
                mt-2
                text-slate-400
              "
            >
              Search Results
            </p>

          </div>

        </div>

        {/* Search Form */}

        <div
          className="
            mt-12
            max-w-3xl
            mx-auto
          "
        >

          <AttorneyForm
            onSubmit={verifyAttorney}
            loading={loading}
          />

        </div>

        {/* Loading */}

        {loading && (

          <div
            className="
              mt-10
              text-center
            "
          >

            <div
              className="
                w-14
                h-14
                mx-auto
                border-4
                border-cyan-400/20
                border-t-cyan-400
                rounded-full
                animate-spin
              "
            />

            <p
              className="
                mt-4
                text-slate-400
              "
            >
              Searching Attorney Records...
            </p>

          </div>

        )}

        {/* Result */}

        {result && (

          <div
            className="
              mt-12
              max-w-4xl
              mx-auto
            "
          >

            <ResultCard
              result={result}
            />

          </div>

        )}

      </div>

    </div>

  );
};

export default Home;

