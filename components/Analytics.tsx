"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
  BarChart3,
  TrendingUp,
  TrendingDown,
  Clock,
  Star,
  AlertTriangle,
  CheckCircle,
  DollarSign,
  Target,
  Activity,
} from "lucide-react"
import { apiService } from "@/lib/api"

interface AnalyticsData {
  employee_satisfaction: number
  schedule_efficiency: number
  total_hours_scheduled: number
  overtime_hours: number
  department_performance: Array<{
    department: string
    efficiency: number
    satisfaction: number
    hours: number
  }>
  monthly_trends: Array<{
    month: string
    efficiency: number
    satisfaction: number
    hours: number
  }>
  ai_insights: Array<{
    type: "success" | "warning" | "info"
    title: string
    description: string
    impact: string
  }>
}

export default function Analytics() {
  const [data, setData] = useState<AnalyticsData | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedPeriod, setSelectedPeriod] = useState("30")
  const [selectedMetric, setSelectedMetric] = useState("efficiency")

  useEffect(() => {
    loadAnalytics()
  }, [selectedPeriod])

  const loadAnalytics = async () => {
    try {
      setLoading(true)

      // In a real app, you would fetch from multiple endpoints
      const response = await apiService.getDashboardAnalytics()

      // Generate comprehensive sample analytics data
      const sampleData: AnalyticsData = {
        employee_satisfaction: 4.2,
        schedule_efficiency: 87,
        total_hours_scheduled: 1240,
        overtime_hours: 45,
        department_performance: [
          {
            department: "Operations",
            efficiency: 92,
            satisfaction: 4.3,
            hours: 480,
          },
          {
            department: "Customer Service",
            efficiency: 85,
            satisfaction: 4.1,
            hours: 360,
          },
          {
            department: "Sales",
            efficiency: 78,
            satisfaction: 3.9,
            hours: 280,
          },
          {
            department: "Management",
            efficiency: 95,
            satisfaction: 4.5,
            hours: 120,
          },
        ],
        monthly_trends: [
          { month: "Oct", efficiency: 82, satisfaction: 3.8, hours: 1180 },
          { month: "Nov", efficiency: 85, satisfaction: 4.0, hours: 1220 },
          { month: "Dec", efficiency: 87, satisfaction: 4.2, hours: 1240 },
          { month: "Jan", efficiency: 89, satisfaction: 4.3, hours: 1280 },
        ],
        ai_insights: [
          {
            type: "success",
            title: "Optimal Schedule Balance Achieved",
            description:
              "Current schedules show excellent work-life balance with 95% employee satisfaction on shift distribution.",
            impact: "High employee retention expected",
          },
          {
            type: "warning",
            title: "Overtime Trending Upward",
            description:
              "Overtime hours increased by 12% this month. Consider hiring additional staff for peak periods.",
            impact: "Potential cost increase of $2,400/month",
          },
          {
            type: "info",
            title: "AI Optimization Opportunity",
            description:
              "Schedule efficiency could improve by 8% by adjusting shift patterns in Customer Service department.",
            impact: "Estimated 15 hours/week savings",
          },
          {
            type: "success",
            title: "Department Performance Excellence",
            description: "Operations department achieved 92% efficiency rating, exceeding target by 7%.",
            impact: "Benchmark for other departments",
          },
        ],
      }

      setData(sampleData)
    } catch (error) {
      console.error("Failed to load analytics:", error)
      // Set minimal fallback data
      setData({
        employee_satisfaction: 4.0,
        schedule_efficiency: 85,
        total_hours_scheduled: 1000,
        overtime_hours: 30,
        department_performance: [],
        monthly_trends: [],
        ai_insights: [],
      })
    } finally {
      setLoading(false)
    }
  }

  const getInsightIcon = (type: string) => {
    switch (type) {
      case "success":
        return <CheckCircle className="w-5 h-5 text-green-500" />
      case "warning":
        return <AlertTriangle className="w-5 h-5 text-yellow-500" />
      case "info":
        return <Activity className="w-5 h-5 text-blue-500" />
      default:
        return <Activity className="w-5 h-5 text-gray-500" />
    }
  }

  const getInsightColor = (type: string) => {
    switch (type) {
      case "success":
        return "border-green-200 bg-green-50"
      case "warning":
        return "border-yellow-200 bg-yellow-50"
      case "info":
        return "border-blue-200 bg-blue-50"
      default:
        return "border-gray-200 bg-gray-50"
    }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-32 bg-gray-200 rounded"></div>
            ))}
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="h-64 bg-gray-200 rounded"></div>
            <div className="h-64 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="text-center py-12">
        <BarChart3 className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-600">Failed to load analytics data</p>
        <Button onClick={loadAnalytics} className="mt-4">
          Retry
        </Button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Analytics & Insights</h1>
          <p className="text-gray-600">Performance metrics and AI-powered insights</p>
        </div>

        <div className="flex gap-2">
          <Select value={selectedPeriod} onValueChange={setSelectedPeriod}>
            <SelectTrigger className="w-32">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="7">Last 7 days</SelectItem>
              <SelectItem value="30">Last 30 days</SelectItem>
              <SelectItem value="90">Last 90 days</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Employee Satisfaction</p>
                <div className="flex items-center gap-2">
                  <p className="text-3xl font-bold text-gray-900">{data.employee_satisfaction.toFixed(1)}</p>
                  <div className="flex">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <Star
                        key={star}
                        className={`w-4 h-4 ${
                          star <= data.employee_satisfaction ? "text-yellow-400 fill-current" : "text-gray-300"
                        }`}
                      />
                    ))}
                  </div>
                </div>
                <div className="flex items-center gap-1 mt-1">
                  <TrendingUp className="w-4 h-4 text-green-500" />
                  <span className="text-sm text-green-600">+0.3 from last month</span>
                </div>
              </div>
              <div className="p-3 rounded-full bg-yellow-50">
                <Star className="w-6 h-6 text-yellow-500" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Schedule Efficiency</p>
                <p className="text-3xl font-bold text-gray-900">{data.schedule_efficiency}%</p>
                <div className="flex items-center gap-1 mt-1">
                  <TrendingUp className="w-4 h-4 text-green-500" />
                  <span className="text-sm text-green-600">+5% from last month</span>
                </div>
              </div>
              <div className="p-3 rounded-full bg-blue-50">
                <Target className="w-6 h-6 text-blue-500" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Hours Scheduled</p>
                <p className="text-3xl font-bold text-gray-900">{data.total_hours_scheduled.toLocaleString()}</p>
                <div className="flex items-center gap-1 mt-1">
                  <TrendingUp className="w-4 h-4 text-green-500" />
                  <span className="text-sm text-green-600">+2% from last month</span>
                </div>
              </div>
              <div className="p-3 rounded-full bg-green-50">
                <Clock className="w-6 h-6 text-green-500" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Overtime Hours</p>
                <p className="text-3xl font-bold text-gray-900">{data.overtime_hours}</p>
                <div className="flex items-center gap-1 mt-1">
                  <TrendingDown className="w-4 h-4 text-red-500" />
                  <span className="text-sm text-red-600">+12% from last month</span>
                </div>
              </div>
              <div className="p-3 rounded-full bg-red-50">
                <AlertTriangle className="w-6 h-6 text-red-500" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Department Performance */}
        <Card>
          <CardHeader>
            <CardTitle>Department Performance</CardTitle>
            <CardDescription>Efficiency and satisfaction by department</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {data.department_performance.map((dept, index) => (
              <div key={index} className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-medium">{dept.department}</span>
                  <div className="flex items-center gap-4 text-sm">
                    <span className="text-gray-600">{dept.hours}h</span>
                    <Badge variant="secondary">{dept.efficiency}% efficient</Badge>
                  </div>
                </div>
                <div className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span>Efficiency</span>
                    <span>{dept.efficiency}%</span>
                  </div>
                  <Progress value={dept.efficiency} className="h-2" />
                </div>
                <div className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span>Satisfaction</span>
                    <span>{dept.satisfaction}/5</span>
                  </div>
                  <Progress value={(dept.satisfaction / 5) * 100} className="h-2" />
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Monthly Trends */}
        <Card>
          <CardHeader>
            <CardTitle>Monthly Trends</CardTitle>
            <CardDescription>Performance trends over the last 4 months</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {data.monthly_trends.map((trend, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="font-medium">{trend.month}</div>
                  <div className="flex items-center gap-4 text-sm">
                    <div className="text-center">
                      <div className="text-gray-600">Efficiency</div>
                      <div className="font-medium">{trend.efficiency}%</div>
                    </div>
                    <div className="text-center">
                      <div className="text-gray-600">Satisfaction</div>
                      <div className="font-medium">{trend.satisfaction}</div>
                    </div>
                    <div className="text-center">
                      <div className="text-gray-600">Hours</div>
                      <div className="font-medium">{trend.hours}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* AI Insights */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="w-5 h-5 text-purple-500" />
            AI-Powered Insights
          </CardTitle>
          <CardDescription>Intelligent recommendations based on your scheduling data</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {data.ai_insights.map((insight, index) => (
              <div key={index} className={`p-4 rounded-lg border ${getInsightColor(insight.type)}`}>
                <div className="flex items-start gap-3">
                  {getInsightIcon(insight.type)}
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900 mb-1">{insight.title}</h4>
                    <p className="text-sm text-gray-600 mb-2">{insight.description}</p>
                    <div className="text-xs text-gray-500">
                      <strong>Impact:</strong> {insight.impact}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Cost Analysis */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <DollarSign className="w-5 h-5 text-green-500" />
            Cost Analysis
          </CardTitle>
          <CardDescription>Labor cost breakdown and optimization opportunities</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-gray-900">$24,800</div>
              <div className="text-sm text-gray-600">Regular Hours</div>
              <div className="text-xs text-green-600 mt-1">Within budget</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-orange-600">$1,350</div>
              <div className="text-sm text-gray-600">Overtime Costs</div>
              <div className="text-xs text-orange-600 mt-1">12% increase</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-gray-900">$26,150</div>
              <div className="text-sm text-gray-600">Total Labor Cost</div>
              <div className="text-xs text-blue-600 mt-1">2% under projection</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
