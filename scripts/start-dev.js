const { spawn } = require("child_process")
const path = require("path")
const os = require("os")

console.log("🚀 Starting Automated Schedule Planner Development Environment...\n")

// Determine the correct command based on OS
const isWindows = os.platform() === "win32"
const pythonCmd = isWindows ? "python" : "python3"
const npmCmd = isWindows ? "npm.cmd" : "npm"

// Start backend
console.log("📡 Starting Python Backend...")
const backendPath = path.join(__dirname, "..", "backend")

const backend = spawn(pythonCmd, ["main.py"], {
  cwd: backendPath,
  stdio: "inherit",
  shell: true,
})

backend.on("error", (err) => {
  console.error("❌ Backend error:", err)
  console.log("\n🔧 Troubleshooting:")
  console.log("1. Make sure Python is installed and in PATH")
  console.log("2. Navigate to backend directory: cd backend")
  console.log("3. Install dependencies: pip install -r requirements.txt")
  console.log("4. Run manually: python main.py")
})

// Wait for backend to start
setTimeout(() => {
  console.log("\n🌐 Starting Next.js Frontend...")

  const frontend = spawn(npmCmd, ["run", "dev"], {
    stdio: "inherit",
    shell: true,
  })

  frontend.on("error", (err) => {
    console.error("❌ Frontend error:", err)
    console.log("\n🔧 Troubleshooting:")
    console.log("1. Make sure Node.js is installed")
    console.log("2. Run: npm install")
    console.log("3. Run manually: npm run dev")
  })

  // Handle cleanup
  process.on("SIGINT", () => {
    console.log("\n🛑 Shutting down development environment...")
    backend.kill()
    frontend.kill()
    process.exit()
  })
}, 5000)

console.log("\n📖 Once started:")
console.log("- Frontend: http://localhost:3000")
console.log("- Backend API: http://localhost:8000/docs")
console.log("- Health Check: http://localhost:8000/api/health")
console.log("\n🔐 Demo Login:")
console.log("- Admin: admin@asp.com / admin123")
console.log("- Employee: demo@asp.com / demo123")
